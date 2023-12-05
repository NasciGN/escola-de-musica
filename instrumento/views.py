from django.urls import reverse_lazy
from core.models import Instrumento
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
<<<<<<< HEAD
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
=======
from django.utils import translation
from django.utils.translation import gettext as _
>>>>>>> 9abfeb55dfbbcc181b992feca2d97b1cd5563ebf

class InstrumentoListView(LoginRequiredMixin, ListView):
    model = Instrumento
    template_name = 'instrumento/tabela_instrumento.html'
    context_object_name = 'instrumentos'
    login_url = 'login'

class InstrumentoCreateView(LoginRequiredMixin, CreateView):
    model = Instrumento
    template_name = 'instrumento/criar_instrumento.html'
    fields = ['nome', 'marca', 'modelo', 'n_serie', 'musico']
    success_url = reverse_lazy('instrumento:read')
    login_url = 'login'

class InstrumentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Instrumento
    template_name = 'instrumento/criar_instrumento.html'
    fields = ['nome', 'marca', 'modelo', 'n_serie', 'musico']
    success_url = reverse_lazy('instrumento:read')
    slug_field = 'id'
    login_url = 'login'

class InstrumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Instrumento
    success_url = reverse_lazy('instrumento:read')
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
<<<<<<< HEAD
        return redirect(self.get_success_url())


class GerarPdfTableSinfoniaView(LoginRequiredMixin, View):
    permission_required = 'core.view_instrumento'

    def get(self, request):
        try:
            instrumentos = Instrumento.objects.all()
            if not instrumentos.exists():
                return HttpResponse('Não há instrumentos cadastradas')
            
            template = get_template('instrumento/instrumento_pdf.html')
            contexto = {'instrumentos': instrumentos}
            html = template.render(contexto)
            
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="instrumentos.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            
            if pisa_status.err:
                return HttpResponse('Erro ao gerar o PDF')
            
            return response
        except Sinfonia.DoesNotExist:
            return HttpResponse('Erro ao recuperar instrumentos')


=======
        return redirect(self.get_success_url())
>>>>>>> 9abfeb55dfbbcc181b992feca2d97b1cd5563ebf
