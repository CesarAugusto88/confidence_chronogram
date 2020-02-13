from django.shortcuts import render, redirect
from confidence_chronograms.models import Chronogram
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User

from confidence_chronograms.models import Chronogram

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
            return redirect('/')

        messages.error(request, "Usuário ou senha inválida.")
    
    return redirect('/')

@login_required(login_url='/login/')
def list_chronograms(request):
    """ retorna cronogramas
    """
    usuario = request.user
    chronogram = Chronogram.objects.filter(usuario=usuario)
    # comando 'for' no html -> for chronogram in chronograms:
    dados = {'chronograms': chronogram}
    
    #return HttpResponse('Olá Django')
    return render(request, 'chronogram.html', dados)