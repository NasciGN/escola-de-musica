from django import forms
from django.urls import reverse_lazy
from core.models import Apresentacao
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.views import View
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

class ApresentacaoListView(LoginRequiredMixin, ListView):
    model = Apresentacao
    template_name = 'apresentacao/tabela_apresentacao.html'
    context_object_name = 'apresentacoes'
    login_url = 'login'


class ApresentacaoCreateView(LoginRequiredMixin, CreateView):
    model = Apresentacao
    template_name = 'apresentacao/criar_apresentacao.html'
    fields = ['nome', 'orquestra', 'sinfonia', 'dt_apresentacao']
    success_url = reverse_lazy('apresentacao:read')
    login_url = 'login'


class ApresentacaoForm(forms.ModelForm):
    class Meta:
        model = Apresentacao
        fields = ['nome', 'orquestra', 'sinfonia', 'dt_apresentacao']
        widgets = {
            'dt_apresentacao': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'nome': _('Name'),
            'orquestra': _('Orchestra'),
            'sinfonia': _('Symphony'),
            'dt_apresentacao': _('Date of Presentation'),
        }

class ApresentacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Apresentacao
    template_name = 'apresentacao/criar_apresentacao.html'
    form_class = ApresentacaoForm
    success_url = reverse_lazy('apresentacao:read')
    slug_field = 'id'
    login_url = 'login'


class ApresentacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Apresentacao
    success_url = reverse_lazy('apresentacao:read')
    login_url = 'login'


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

class GerarPdfTableApresentacaoView(LoginRequiredMixin, View):
    permission_required = 'core.view_'

    def get(self, request):
        try:
            apresentacoes = Apresentacao.objects.all()
            if not apresentacoes.exists():
                return HttpResponse('Não há apresentacoes cadastradas')
            
            template = get_template('apresentacao/apresentacao_pdf.html')
            contexto = {'apresentacoes': apresentacoes}
            html = template.render(contexto)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="apresentacoes.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            
            if pisa_status.err:
                return HttpResponse('Erro ao gerar o PDF')
            
            return response
        except Apresentacao.DoesNotExist:
            return HttpResponse('Erro ao recuperar apresentacoes')

