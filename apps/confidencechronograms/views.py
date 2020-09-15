from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User
import json
from apps.confidencechronograms.models import Task, Cliente, Funcionario, Chronogram
from apps.confidencechronograms.forms import TaskForm, ChronogramForm


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
            return redirect('/confidencechronogram/')
        messages.error(request, "Usuário ou senha inválida.")
        
    return redirect('/login/')

# enviar direto para user (funcionario/cliente)
@login_required(login_url="/login/")
def confidencechronogram(request):
    """ Verifica se é funcionario ou cliente."""
    usuario = request.user
    # select * from Funcionario where usuario_fun = usuario;
    funcionario = Funcionario.objects.filter(usuario_fun=usuario)

    if funcionario:
        return redirect("/confidencechronogram/funcionario")
    else:
        #return redirect("/confidencechronogram/cliente")
        return redirect("/confidencechronogram/cliente")

# lista as tarefas do chronograma para o cliente
@login_required(login_url='/login/')
def list_chronogram(request):
    """ retorna o cronograma com às tarefas (javascript)
    Mostrar o caminho crítico das atividades do cronograma: Atividades que não podem
      atrasar - As atividades ja vão estar no limite.
    Mostrar a porcentagem da conclusão das atividades para o cliente ter uma visão.
    javascript? Mostrar a porcentagem do valor investido conforme o valor 
    total do models Chronogram.
    """
    cliente = request.user
    try:
        cliente = Cliente.objects.get(usuario_cli=cliente)
        # filter mostra como está a saida em __str__
        # do models da classe
        #cronograma = Chronogram.objects.filter(client=cliente)
        # get mostra od atributos do objeto
        # e assim pope-se colocar qual atributo
        cronograma = Chronogram.objects.get(client=cliente)

    except Exception:
        raise Http404()
   
    if cliente:
        #print(cronograma.id)
        #c = Chronogram.objects.first()
        #c = request.user.chronogram_set.get()

        tasks = [t.to_dict() for t in Task.objects.filter(chronogram=cronograma.id)]

        context = {
            "tasks": json.dumps(tasks), "cliente": cliente, 'cronograma': cronograma
        }

    elif not cliente:
        messages.info(request, 'Usuário diferente, contate um administrados!')
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


###############################################

# -------Cliente--------------------------
# Cliente vai ver seus dados e pode editar

@login_required(login_url="/login/")
def dados_cliente(request):
    """ Mostra dados do cliente."""
    usuario_cli = request.user
    try:
        # Mesmo objeto em html
        cliente = Cliente.objects.filter(usuario_cli=usuario_cli)
        # cliente = Cliente.objects.all()
    except Exception:
        raise Http404()
    if cliente:
        # variáveis usadas no html:
        dados = {"cliente": cliente}
    else:
        raise Http404()

    return render(request, "confidence-cliente.html", dados)

@login_required(login_url="/login/")
def cliente(request):
    dados = {}
    # pegar usuario solicitando
    usuario = request.user
    id_cliente = request.GET.get("id")
    if id_cliente:
        cliente = Cliente.objects.get(id=id_cliente)
        # se o mesmo cliente.usuario_cliid igual ao usuario
        # solicitando para restringir qualquer user ver os dados com o id
        if cliente.usuario_cli == usuario:
            dados["cliente"] = Cliente.objects.get(id=id_cliente)
    return render(request, "cliente.html", dados)

# editar cliente
@login_required(login_url="/login/")
def submit_cliente(request):

    if request.POST:
        nome = request.POST.get("nome")
        fone1 = request.POST.get("fone1")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")

        usuario_cli = request.user
        id_cliente = request.POST.get("id_cliente")
        if id_cliente:
            cliente = Cliente.objects.get(id=id_cliente)
            if cliente.usuario_cli == usuario_cli:
                cliente.nome = nome
                cliente.fone1 = fone1
                cliente.endereco = endereco
                cliente.cidade = cidade
                cliente.cep = cep
                cliente.uf = uf
                cliente.save()
        
    return redirect("/confidencechronogram/cliente")


@login_required(login_url="/login/")
def delete_cliente(request, id_cliente):
    usuario_cli = request.user
    try:
        cliente = Cliente.objects.get(id=id_cliente)
    except Exception:
        raise Http404()
    if usuario_cli == cliente.usuario_cli:
        cliente.delete()
    else:
        raise Http404()
    return redirect("/confidencechronogram")


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor
# @login_required(login_url='/login/')
def json_lista_cliente(request, id_usuario):
    # request.user
    usuario_cli = User.objects.get(id=id_usuario)
    cliente = Cliente.objects.filter(usuario_cli=usuario_cli).values(
        "id", "nome"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(cliente), safe=False)


# PARA ACESSAR SOMENTE DA TABELA CORRESPONDENTE COM SOMENTE SEUS DADOS(hacker pode ver com ids)

# FUNCIONÁRIOS
# Mudado nome de lista_funcionarios para dados_funcionario
@login_required(login_url="/login/")
def dados_funcionario(request):
    """ Lista dados do funcionário."""
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.filter(usuario_fun=usuario_fun)

    except Exception:
        raise Http404()

    #if funcionario:
    if funcionario:
        # variáveis usadas no html:
        #Mudando variáveis e rotas...
        dados = {"funcionario": funcionario}

    else:
        raise Http404()

    return render(request, "confidence-funcionario.html", dados)


@login_required(login_url="/login/")
def funcionario(request):
    dados = {}
    #pegar usuário solicitando
    usuario = request.user
    id_funcionario = request.GET.get("id")
    if id_funcionario:
        funcionario = Funcionario.objects.get(id=id_funcionario)
        # se o mesmo funcionario.usuario_fun id igual ao usuario
        # solicitando para restringir qualquer user ver os dados com o id
        if funcionario.usuario_fun == usuario:
            dados["funcionario"] = Funcionario.objects.get(id=id_funcionario)

    return render(request, "funcionario.html", dados)

# edita funcionario
@login_required(login_url="/login/")
def submit_funcionario(request):
    if request.POST:
        nome = request.POST.get("nome")
        fone1 = request.POST.get("fone1")
        endereco = request.POST.get("endereco")
        cidade = request.POST.get("cidade")
        cep = request.POST.get("cep")
        uf = request.POST.get("uf")

        usuario_fun = request.user
        id_funcionario = request.POST.get("id_funcionario")
        if id_funcionario:
            funcionario = Funcionario.objects.get(id=id_funcionario)
            if funcionario.usuario_fun == usuario_fun:
                funcionario.nome = nome
                funcionario.fone1 = fone1
                funcionario.endereco = endereco
                funcionario.cidade = cidade
                funcionario.cep = cep
                funcionario.uf = uf

                funcionario.save()
        # Evento.objects.filter(id=id_funcionario).update(nome=nome, endereco=endereco,fone1=fone1)
        
    return redirect("/confidencechronogram/funcionario")


# REDIRECIONAR CORRETAMENTE
@login_required(login_url="/login/")
def delete_funcionario(request, id_funcionario):
    # Fazer verificações como esta nas outras funções.
    usuario_fun = request.user
    try:
        funcionario = Funcionario.objects.get(id=id_funcionario)
    except Exception:
        raise Http404()
    if usuario_fun == funcionario.usuario_fun:
        funcionario.delete()
    else:
        raise Http404()
    return redirect("/confidencechronogram") 


# retornar JsonResponse para trabalhar com JavaScript, Ajax...
# para pegar por usuário (id), sem decoretor
@login_required(login_url="/login/")
def json_lista_funcionario(request, id_usuario_fun):
    # request.user
    usuario_fun = User.objects.get(id=id_usuario_fun)
    funcionario = Funcionario.objects.filter(usuario_fun=usuario_fun).values(
        "id", "nome"
    )
    # safe=False porque nao é dicionário.
    return JsonResponse(list(funcionario), safe=False)

#########################################
# Criar Cronograma, Listar Cronogramas, Deletar-não.
@login_required(login_url="/login/")
def chronogram_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
        
    except Exception:
        raise Http404()

    if funcionario:
        cronogramas = Chronogram.objects.all()
        dados = {"cronogramas": cronogramas}
    else:
        raise Http404()

    return render(request, "chronogram_list.html", dados)


@login_required(login_url="/login/")
def new_chronogram(request):
    """ Cria formulário do cronograma e envia objeto cliente.
    """

    #print(usuario_cli)
    if request.method == "POST":
        form = ChronogramForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            assunto = form.cleaned_data['assunto']
            descricao = form.cleaned_data['descricao']
            arquivo = form.cleaned_data['arquivo']
            funcionario = form.cleaned_data['funcionario']
            cliente = form.cleaned_data['cliente']
            novo = Chronogram(
                titulo=titulo, assunto=assunto, descricao=descricao,
                arquivo=arquivo, funcionario=funcionario, cliente=cliente 
            )
            novo.save()
            #form.save()
            return redirect("funcionario")
    else:
        form = ChamadoForm()
    return render(request, "criar_cronograma.html", {"form": form})


@login_required(login_url="/login/")
def delete_chronogram(request, pk):
    if request.method == "POST":
        chronogram = Chronogram.objects.get(pk=pk)
        chronogram.delete()
    return redirect("funcionario")



