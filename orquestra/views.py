from django.urls import reverse_lazy
from core.models import Orquestra
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View

class OrquestraListView(LoginRequiredMixin, ListView):
    model = Orquestra
    template_name = 'orquestra/tabela_orquestra.html'
    context_object_name = 'orquestras'
    login_url='login'

class OrquestraCreateView(LoginRequiredMixin, CreateView):
    model = Orquestra
    template_name = 'orquestra/criar_orquestra.html'
    fields = ['nome', 'cidade', 'pais', 'musicos']
    success_url = reverse_lazy('orquestra:read')
    login_url='login'
    

class OrquestraUpdateView(LoginRequiredMixin, UpdateView):
    model = Orquestra
    template_name = 'orquestra/criar_orquestra.html'
    fields = ['nome', 'cidade', 'pais', 'musicos']
    success_url = reverse_lazy('orquestra:read')
    slug_field = 'id'
    login_url='login'

class OrquestraDeleteView(LoginRequiredMixin, DeleteView):
    model = Orquestra
    success_url = reverse_lazy('orquestra:read')
    login_url='login'
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())

class GerarPdfTableOrquestraView(LoginRequiredMixin, View):
    permission_required = 'core.view_orquestra'

    def get(self, request):
        try:
            orquestras = Orquestra.objects.all()
            if not orquestras.exists():
                return HttpResponse('Não há orquestras cadastradas')
            
            template = get_template('orquestra/orquesta_pdf.html')
            contexto = {'orquestras': orquestras}
            html = template.render(contexto)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="orquestras.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            
            if pisa_status.err:
                return HttpResponse('Erro ao gerar o PDF')
            
            return response
        except Orquestra.DoesNotExist:
            return HttpResponse('Erro ao recuperar orquestras')
