from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    #path('registrar/', views.register.as_view(), name='registrar'),
    # Registra USUARIO cliente/funcionario
    path('registrar/clie', views.register_clie, name='registrar_cliente'),
    path('cadastro/cliente', views.register_cliente, name='register_cliente'),
    path('cadastro/submit', views.submit_register_cliente),
    
    path('registrar/func', views.register_func, name='registrar_funcionario'),    
    path('funcionario', views.register_funcionario, name='register_funcionario'),
    path('submit', views.submit_register_funcionario),
]