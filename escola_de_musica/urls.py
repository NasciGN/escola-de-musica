from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from core import views
from escola_de_musica import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin:index'),
    path('', views.IndexView.as_view(), name='home'),
    path('sinfonia/', include('sinfonia.urls')),
    path('instrumentos/', include('instrumento.urls')),
    path('orquestras/', include('orquestra.urls')),
    path('apresentacoes/', include('apresentacao.urls')),
    path('musico/', include('musico.urls')),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.logar, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('sobre/', views.SobreView.as_view(), name='sobre'),
    path('change-language/<str:language>/', views.change_language, name='change_language'),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
