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
    #Lista (tarefas) do cronograma
    path('chronogram/', views.list_chronogram, name='list_chronogram'),
    #path('', views.index)
    # Se encontrar url vazia(normal, local), redireciona para chronogram
    #path('', RedirectView.as_view(url='/chronogram/')),
    path('login/', views.login_user, name='login_user'),
    path('login/submit', views.submit_login, name='submit_login'),
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
    ##################################################################################################
    # Cronograma - com busca
    path("confidencechronogram/chronogram/", views.chronogram_list, name="chronogram_list"),
    path("confidencechronogram/chronogram/newchronogram/", views.new_chronogram, name="new_chronogram"),
    path("confidencechronogram/chronogram/update/<int:id>/", views.update_chronogram, name="update_chronogram"),
    path("confidencechronogram/chronogram/delete/<int:id>/", views.delete_chronogram, name="delete_chronogram"),
    # Tarefa - com busca
    path("confidencechronogram/task/", views.task_list, name="task_list"),
    path("confidencechronogram/task/newtask/", views.new_task, name="new_task"),
    path("confidencechronogram/task/update/<int:id>/", views.update_task, name="update_task"),
    path("confidencechronogram/task/delete/<int:id>/", views.delete_task, name="delete_task"),
    # ------------Comentário-Cliente-------------------------------------------
    path("confidencechronogram/uploadcomentario/", views.uploadcomentario, name="uploadcomentario"),
    path("confidencechronogram/comentarios/", views.comentario_list, name="comentario_list"),
    path("confidencechronogram/comentarios/criarcomentarios/", views.criar_comentario, name="criar_comentario"),
    path("confidencechronogram/comentarios/update/<int:id>/", views.update_comentario, name="update_comentario"),
    path("confidencechronogram/comentarios/delete/<int:id>/", views.delete_comentario, name="delete_comentario"),
    #visualizar a lista de comentarios pelo funcionario também
    path("confidencechronogram/comentarios/funcionario", views.comentario_list_fun, name="comentario_list_fun"),
    #Valores de tarefas
    path("confidencechronogram/task/price", views.price_task, name="price_task"),
    #Email-views
    #path("confidencechronogram/sendmail", views.e_mail, name="e_mail"),
    
    #relatório PDF
    re_path(r'^pdf/$', views.GeneratePDF.as_view(), name="relatorio"),

    # Para aparecer arquivos do diretório media quando DEBUG=False
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
