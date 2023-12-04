### O que eu tentei
1. Idiomas
    ### Definir quais idiomas irá usar no arquivo `settings.py`
    ```py
    # necessario colocar pt-br pra ele não dar erro com LANGUAGE_CODE
    LANGUAGES = [
        ('en', ('English')),
        ('pt-br', ('Portuguese')),
    ]
    ```
    ### É necessario instalar essa bibliotéca para que funcione os demais comandos
    ```sh
    sudo apt-get install gettext
    ```
    ### criar os arquivos .po
    ```sh
    python manage.py makemessages -l pt
    python manage.py makemessages -l en
    ```
    ### criar os arquivos .mo
    ```sh
    python manage.py compilemessages
    ```
    Os arquivos django.po e django.mo estão dentro de:  
    /PROG-ESCOLA-MUSICA/locale/en/LC_MESSAGES  
    /PROG-ESCOLA-MUSICA/locale/pt/LC_MESSAGES
    ### Arquivos views.py do core
    ```py
    # views.py
    from django.shortcuts import render
    from django.utils import translation

    def change_language(request, language):
        if language in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
        return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirecione de volta para a página anterior ou 'home'.
    ```
    ### Arquivos urls.py do core
    ```py
    # urls.py
    from django.urls import path
    from .views import change_language

    urlpatterns = [
        # ... outras URLs ...
        path('change-language/<str:language>/', change_language, name='change_language'),
    ]
    ```
    ### Arquivos lenguage_selector.html do core
    O caminho é core/template/components/lenguage_selector.html
    ```html
    <!-- templates/language_selector.html -->
    <form action="{% url 'change_language' language_code %}" method="post">
        {% csrf_token %}
        <select name="language_code" onchange="this.form.submit()">
            {% for lang_code, lang_name in LANGUAGES %}
                <option value="{{ lang_code }}" {% if lang_code == request.LANGUAGE_CODE %}selected{% endif %}>{{ lang_name }}</option>
            {% endfor %}
        </select>
    </form>
    ```
    ### implementar no arquivo nav_menu.html
    ```html
    <!-- Seletor de Idioma -->
    <div class="col-lg-2" data-aos-duration="600" data-aos="fade-down" data-aos-delay="0">
        {% include 'language_selector.html' %}
    </div>
    ```
2. Gerar PDF
    ### Arquivo views.py de sinfonia
    ```py
    class GerarPDFSinfoniaView(PermissionRequiredMixin, View):
    permission_required = 'core.view_sinfonia'
    def get(self, request, sinfonia_id):
        try:
            sinfonia = get_object_or_404(Sinfonia, pk=sinfonia_id)
            template = get_template('sinfonia_template.html')
            contexto = {'sinfonia': sinfonia}
            html = template.render(contexto)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'filename="{sinfonia.nome}_relatorio.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Erro ao gerar o PDF')
            return response
        except Sinfonia.DoesNotExist:
            return HttpResponse('Sinfonia não encontrada')
    ```
    ### Adicionar essa linha no urls.py
    ```py
    path('gerar_pdf_sinfonia/<int:sinfonia_id>/', views.GerarPDFSinfoniaView.as_view(), name='gerar_pdf_sinfonia'),
    ```
    ### Adicionar essa linha no arquivo tabela_sinfonia.html 
    ```html
    <td>
        <a href="{% url 'sinfonia:gerar_pdf_sinfonia' sinf.id %}">Gerar PDF</a>
    </td>
    ```
# Escola de Música
### Alunos
- Gabriel Nascimento
- Isaías Félix
- Murilo José
- Thauan Felipe
***
### Requisitos trabalho final `programação IV`
O trabalho consiste em criar uma aplicação web utilizando o framework Django e deverá conter os seguintes itens:
1. [x] O sistema deverá ter no mínimo dois níveis de usuários e deverá haver páginas que vão ser acessíveis a um determinado tipo de usuário.
1. [ ] O sistema deverá gerar pelo menos uma relação em PDF.
1. [ ] O sistema deverá gerar pelo menos uma aplicação de AJAX.
1. [x] O sistema deverá ter um visual agradável para os usuários.
1. [ ] O sistema deve estar disponível em pelo menos mais um idioma.
1. [x] O sistema deve permitir interação dos usuários, seja para se cadastrar no site, seja para mudar o visual do sistema, ou outra interação pertinente.
1. [ ] O sistema deve se preocupar com a acessibilidade (principalmente para deficientes visuais).
***
### Sobre a atividade
Este é um projeto de um sistema web desenvolvido em Django e Bootstrap/HTML, criado para gerenciar orquestras, músicos, instrumentos, apresentações, sinfonias e suas respectivas associações.
### Funcionalidades
- Adicionar, visualizar, editar e excluir instrumentos musicais, atribuindo um músico para utiliza-lo temporariamente.
- Gerenciar músicos, incluindo a associação com um instrumento específico.
- Registrar e gerenciar apresentações musicais, incluindo a data e hora.
- Criar sinfonias e associá-las ao seu compositor.
- Gerenciar orquestras, incluindo a adição e remoção de músicos, apresentações e sinfonias.
***
### Tecnologias Utilizadas
- Django: Framework web em Python para o desenvolvimento do backend.
- Bootstrap/HTML: Utilizados para criar o frontend responsivo e amigável ao usuário.
***
### Permissões
- O sistema foi planejado com algumas permissões específicas para cada usuário.
***
### Super usuário
Usuário: admin  
Senha: admin
### Usuario de teste
Usuário: teste-usuario  
Senha: alunoifro
### Usuario de professor
Usuário: teste-professor  
Senha: alunoifro
### Usuário comum
O usuário comum é aquele que cria sua conta pela inteface de login do site. Todo usuário criado pela interface do site por padrão possui as permissões de usuário comum.   
Este usuário tem permissão para realizar o CRUD completo nas seguintes models:

- Apresentação
- Instrumento
- Orquestra

Para as outras duas models (Músicos e Sinfonias), este usuário só tem permissão de visualização.
***
### Configuração do Ambiente
1. Criar virtual env 
```sh
python -m venv env
```
2. Criar virtual env 
```sh
pip install -r requirements.txt
```
3. Arquivo requirements
```txt
asgiref==3.7.2
Django==4.2.2
django-crispy-forms==2.0
django-jazzmin==2.6.0
sqlparse==0.4.4
tzdata==2023.3
```
4. Criar virtual env 
```sh
python manage.py runserver
```
Acesse o sistema através do URL [http://localhost:8000/](http://localhost:8000/).
***
### Desenvolvimento - Atividades a serem realizadas
- Models
    - [x] Criar o modelo Instrumento.
    - [x] Criar o modelo Musico.
    - [x] Criar o modelo Apresentacao.
    - [x] Criar o modelo Sinfonia.
    - [x] Criar o modelo Orquestra.
- Instrumentos
    - [x] Implementar views para adicionar, visualizar, editar e excluir instrumentos.
    - [x] Configurar as URLs correspondentes para as views de instrumentos.
- Músicos
    - [x] Implementar views para adicionar, visualizar, editar e excluir músicos.
    - [x] Configurar as URLs correspondentes para as views de músicos.
- Apresentações
    - [x] Implementar views para adicionar, visualizar, editar e excluir apresentações.
    - [x] Configurar as URLs correspondentes para as views de apresentações.
- Sinfonias
    - [x] Implementar views para adicionar, visualizar, editar e excluir sinfonias.
    - [x] Configurar as URLs correspondentes para as views de sinfonias.
- Orquestras
    - [x] Implementar views para adicionar, visualizar, editar e excluir orquestras.
    - [x] Configurar as URLs correspondentes para as views de orquestras.
***
### Contribuição
Se você deseja contribuir para o projeto, siga as etapas abaixo:
1. Faça um fork do repositório.
2. Crie uma branch para a sua feature (`git checkout -b feature/nome-da-feature`).
3. Implemente as alterações.
4. Faça o commit das suas alterações (`git commit -m 'Adiciona uma nova feature'`).
5. Faça o push para a branch (`git push origin feature/nome-da-feature`).
6. Abra um Pull Request.
