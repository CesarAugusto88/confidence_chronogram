from django.urls import path, re_path
from . import views
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    #--------------redireciona para HOME---------------------------
    path('', views.home, name='home'),
    path('', RedirectView.as_view(url='/home/')),
    path('contato/', views.contact, name='contact'),
    path('chronogram/', views.list_chronogram, name='list_chronogram'),
    #path('', views.index)
    # Se encontrar url vazia(normal, local), redireciona para chronogram
    #path('', RedirectView.as_view(url='/chronogram/')),
    path('login/', views.login_user, name='login_user'),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user, name='logout_user'),

    path("confidencechronogram/", views.confidencechronogram, name="confidencechronogram"),
    # 
    # -----------cliente-----------------------------------------------------
    path("confidencechronogram/cliente", views.dados_cliente, name="cliente"),
    path("confidencechronogram/lista/<int:id_cliente>/", views.json_lista_cliente),
    path("confidencechronogram/clie/", views.cliente),
    path("confidencechronogram/clie/submit", views.submit_cliente),
    #path("confidencechronogram/clie/delete/<int:id_cliente>/", views.delete_cliente, name="del_cliente"),

    #-------------funcionários--------------------------
    path("confidencechronogram/funcionario", views.dados_funcionario, name="funcionario"),
    path("confidencechronogram/lista/<int:id_funcionario>/", views.json_lista_funcionario),
    path("confidencechronogram/func/", views.funcionario),
    path("confidencechronogram/func/submit", views.submit_funcionario),
    #path(
    #    "confidencechronogram/func/delete/<int:id_funcionario>/",
    #    views.delete_funcionario, name="del_funcionario"
    #),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)