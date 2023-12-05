from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from core.models import Sinfonia
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from xhtml2pdf import pisa
    
class SinfoniaListView(LoginRequiredMixin, ListView):
    model = Sinfonia
    template_name = 'sinfonia/tabela_sinfonia.html'
    context_object_name = 'sinfonias'
    login_url='login'
    

class SinfoniaCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Sinfonia
    template_name = 'sinfonia/criar_sinfonia.html'
    fields = ['nome', 'compositor',]
    success_url = reverse_lazy('sinfonia:read')
    login_url='login'
    permission_required = 'core.add_sinfonia'

class SinfoniaUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Sinfonia
    template_name = 'sinfonia/criar_sinfonia.html'
    fields = ['nome', 'compositor']
    success_url = reverse_lazy('sinfonia:read')
    slug_field = 'id'
    login_url='login'
    permission_required = 'core.change_sinfonia'

class SinfoniaDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Sinfonia
    success_url = reverse_lazy('sinfonia:read')
    login_url='login'
    permission_required = 'core.delete_sinfonia'
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.get_success_url())


class GerarPDFSinfoniaView(PermissionRequiredMixin, View):
    permission_required = 'core.view_sinfonia'

    def get(self, request):
        try:
            sinfonias = Sinfonia.objects.all()
            if not sinfonias.exists():
                return HttpResponse('Não há sinfonia cadastradas')
            
            template = get_template('sinfonia/sinfonia_pdf.html')
            contexto = {'sinfonias': sinfonias}
            html = template.render(contexto)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="sinfonias.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            
            if pisa_status.err:
                return HttpResponse('Erro ao gerar o PDF')
            
            return response
        except Sinfonia.DoesNotExist:
            return HttpResponse('Erro ao recuperar sinfonias')



class GerarPdfTableSinfoniaView(PermissionRequiredMixin, View):
    permission_required = 'core.view_sinfonia'

    def get(self, request):
        try:
            sinfonias = Sinfonia.objects.all()
            if not sinfonias.exists():
                return HttpResponse('Não há sinfonias cadastradas')
            
            template = get_template('sinfonia/sinfonia_template.html')
            contexto = {'sinfonias': sinfonias}
            html = template.render(contexto)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="relatorio_sinfonias.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            
            if pisa_status.err:
                return HttpResponse('Erro ao gerar o PDF')
            
            return response
        except Sinfonia.DoesNotExist:
            return HttpResponse('Erro ao recuperar sinfonias')

