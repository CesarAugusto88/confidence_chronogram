from django.shortcuts import render, redirect
from django.http import HttpResponse

from confidence_chronograms.models import Chronogram

#def index(request):
#    return redirect('/chronogram/')

def list_chronograms(request):
    """ retorna cronogramas
    """
    usuario = request.user
    chronogram = Chronogram.objects.filter(usuario=usuario)
    # comando 'for' no html -> for chronogram in chronograms:
    dados = {'chronograms': chronogram}
    
    #return HttpResponse('Olá Django')
    return render(request, 'chronogram.html', dados)