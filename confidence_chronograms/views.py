from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from confidence_chronograms.models import Chronogram
# from datetime import datetime, timedelta
# from django.http.response import Http404, JsonResponse
# from django.contrib.auth.models import User
import json
from confidence_chronograms.models import Task, Cliente


#def index(request):
#    return redirect('/chronogram/')

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/chronogram/')

        messages.error(request, "Usuário ou senha inválida.")
    
    return redirect('/login/')

@login_required(login_url='/login/')
def list_chronogram(request):
    """ retorna o cronograma com às tarefas (javascript)
    Mostrar o caminho crítico das atividades do cronograma: Atividades que não podem
      atrasar - As atividades ja vão estar no limite.
    Mostrar a porcentagem da conclusão das atividades para o cliente ter uma visão. javascript?
    Mostrar a porcentagem do valor investido conforme o valor total do models Chronogram.
    Exemplo como pegar tarefa do models com usuário específico:
    usuario = request.user
    if usuario...
    tasks = [{ ...}]
    task = Task.objects.filter(usuario=usuario,
                               task_text=tasks...)
    dados = {'tasks':task}
    return render(request, 'chronogram.html', dados)
    """
    # usar variáveis do models Task para usar aqui.
    # Usando listcompression pegando todas as tarefas que está em 
    # Task(models.py) usando a função to_dict()...

    usuario = request.user
    try:
        cliente = Cliente.objects.filter(usuario_cli=usuario)

    except Exception:
        raise Http404()
   
    if cliente:
        tasks = [t.to_dict() for t in Task.objects.all()]

        context = {
            "tasks": json.dumps(tasks),
        }

    elif not cliente:
        messages.info(request, 'Usuário diferente de cliente!')
        return redirect('/login/')

    else:
        raise Http404()
    
    return render(request, "chronogram.html", context)
    
    # antigo:
    # tasks = [
    #     {
    #         "id": "1",
    #         "name": "Instalações preliminares de água e energia",
    #         "start": "2020-02-19",
    #         "end": "2020-02-21",
    #         "progress": "100",
    #         #"dependencies": "",
    #         "custom_class": "bar-milestone" # optional
    #     },
    #     {
    #         "id": "2",
    #         "name": "Fechamento da Construção",
    #         "start": "2020-02-22",
    #         "end": "2020-02-27",
    #         "progress": "20",
    #         "dependencies": "1",
    #         "custom_class": "bar-milestone" # optional
    #     },
    #     {
    #         "id": "3",
    #         "name": "Gabaríto da Obra",
    #         "start": "2020-02-24",
    #         "end": "2020-03-20",
    #         "progress": "20",
    #         "dependencies": "2",
    #         "custom_class": "bar-milestone" # optional
    #     },
    # ]


def home(request):
	# return HttpResponse('Hello World!')
	# Usando render
	return render(request, 'home.html')


def contact(request):
	return render(request, 'contact.html')