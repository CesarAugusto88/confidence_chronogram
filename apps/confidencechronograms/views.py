from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User
import json
from apps.confidencechronograms.models import Task, Cliente, Funcionario, Chronogram, Comentario
from apps.confidencechronograms.forms import TaskForm, ChronogramForm, ComentarioForm

from django.http import HttpResponse
from django.views.generic import View
import datetime #timedelta

from apps.confidencechronograms.utils import render_to_pdf #created in step 4

from confidencechronogram import settings
from django.core.mail import send_mail



#def index(request):
#    return redirect('/chronogram/')
def home(request):
    # return HttpResponse('Hello World!')
    # Usando render
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

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
        return redirect("funcionario")
    else:
        #return redirect("/confidencechronogram/cliente")
        return redirect("cliente")

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
#
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
    """ Cria formulário do cronograma e envia objeto cliente."""
    if request.method == "POST":
        form = ChronogramForm(request.POST)
        if form.is_valid():
            novo = Chronogram(**form.cleaned_data)
            novo.save()

            return redirect("funcionario")
    else:
        form = ChronogramForm()
    return render(request, "criar_cronograma.html", {"form": form})

#Update Chronogram
@login_required(login_url="/login/")
def update_chronogram(request, id):
    """ Atualiza Cronograma."""
    chronogram = Chronogram.objects.get(id=id)
    form = ChronogramForm(request.POST or None, instance=chronogram)
    if form.is_valid():
        form.save()
        return redirect("chronogram_list")
    return render(request, "chronogram_update.html", {"form": form, 'chronogram': chronogram})

@login_required(login_url="/login/")
def delete_chronogram(request, id):
    if request.method == "POST":
        chronogram = Chronogram.objects.get(id=id)
        chronogram.delete()
    return redirect("chronogram_list")

# Criar Tarefas, Listar tarefas, Deletar-.---------------------
@login_required(login_url="/login/")
def task_list(request):
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        tasks = Task.objects.all()
        dados = {"tasks": tasks}
    else:
        raise Http404()
    return render(request, "task_list.html", dados)

@login_required(login_url="/login/")
def new_task(request):
    """ Cria formulário de tarefa."""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            novo = Task(**form.cleaned_data)
            novo.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "criar_tarefa.html", {"form": form})

#Update task
@login_required(login_url="/login/")
def update_task(request, id):
    """ Atualiza tarefa."""
    task = Task.objects.get(id=id)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect("task_list")
    return render(request, "task_update.html", {"form": form, 'task': task})

@login_required(login_url="/login/")
def delete_task(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()
    return redirect("task_list")


# Comentário do Cliente
# FUNÇÕES DE UPLOAD
@login_required(login_url="/login/")
def uploadcomentario(request):
    """Essa função carrega o arquivo do cliente
       É chamada pelo cliente(específico) enviar o arquivo/comentario para o funcionário"""
    context = {}

    if request.method == "POST":
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context["url"] = fs.url(name)
    return render(request, "uploadcomentario.html", context)

#Lista comentario dos clientes
@login_required(login_url="/login/")
def comentario_list(request):
    """ Lista comentario do Cliente """
    usuario = request.user
    dados = {}
    try:
        cliente = Cliente.objects.get(usuario_cli=usuario)
        # funcionario = Funcionario.objects.all()
    except Exception:
        raise Http404()

    #NÃO ESTÁ PEGANDO O CLIENTE ESPECÍFICO QUE LANÇOU OS comentarioS
    # VERIFICAR TAMBÉM EM OUTRA FUNÇÕES
    if cliente:
        #OK esta pegando so os comentarios referentes ao cliente que criou
        #***É preciso atribuir automaticamente o cliente_ch***
        comentarios = Comentario.objects.filter(cliente=cliente)
        #print(cliente.nome)
        
        # se precisar dos dados do cliente
        dados = {"cliente": cliente, "comentarios": comentarios}
    else:
        raise Http404()

    return render(request, "comentario_list.html", dados)

#Lista comentario para funcionários
@login_required(login_url="/login/")
def comentario_list_fun(request):
    """ Lista comentario Para Funcionário Específico. """
    usuario = request.user
    dados = {}
    try:
        funcionario = Funcionario.objects.get(usuario_fun=usuario)
    except Exception:
        raise Http404()
    if funcionario:
        comentarios = Comentario.objects.filter(funcionario=funcionario)
        dados = {"funcionario": funcionario, "comentarios": comentarios}
    else:
        raise Http404()

    return render(request, "comentario_list_fun.html", dados)



@login_required(login_url="/login/")
def criar_comentario(request):
    """ Cria formulário do comentario e envia objeto cliente para pegar id.
    """
    usuario = request.user
    # é preciso pegar usuario com 'get' para atribuir em cliente de comentario.
    usuario_cli = Cliente.objects.get(usuario_cli=usuario)
    #print(usuario_cli)
    if request.method == "POST":
        form = ComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            novo = Comentario(cliente=usuario_cli, **form.cleaned_data)
            novo.save()
            return redirect("comentario_list")
    else:
        form = ComentarioForm()
    return render(request, "criar_comentario.html", {"form": form})

# Update Comentário
@login_required(login_url="/login/")
def update_comentario(request, id):
    """ Atualiza Comentário."""
    comentario = Comentario.objects.get(id=id)
    form = ComentarioForm(request.POST or None, instance=comentario)
    if form.is_valid():
        form.save()
        return redirect("comentario_list")
    return render(request, "comentario_update.html", {"form": form, 'comentario': comentario})

@login_required(login_url="/login/")
def delete_comentario(request, id):
    if request.method == "POST":
        comentario = Comentario.objects.get(id=id)
        comentario.delete()
    return redirect("comentario_list")

# Valores das tarefas
@login_required(login_url="/login/")
def price_task(request):
    """ Lista de nomes, datas e VALORES das tarefas"""
    context = {}
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

        tasks = Task.objects.filter(chronogram=cronograma.id)
        # se precisar dos dados do cliente
        context = {
            "tasks": tasks, "cliente": cliente, 'cronograma': cronograma
        }
    else:
        raise Http404()
    return render(request, "valores_list.html", context)

class GeneratePDF(View):
    """Gerar pdf de relatório para cliente."""
    def get(self, request, *args, **kwargs):
        context = {}
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
            tasks = Task.objects.filter(chronogram=cronograma.id)
            # se precisar dos dados do cliente
            context = {
                "tasks": tasks, "cliente": cliente, "chronogram": cronograma, 
                "today": datetime.date.today()
            }
            # data = {
            #     'today': datetime.date.today(), 
            #     'amount': 39.99,
            #     'customer_name': 'Cooper Mann',
            #     'order_id': 1233434,
            # }
            pdf = render_to_pdf('relatorio.html', context)

            
        else:
            raise Http404()
        
        return HttpResponse(pdf, content_type='confidencechronograms/pdf')


# EMAIL
# def e_mail(request):
#     subject = "Real programmer contact"
#     msg = "Congratulations for your success"
#     to = "cesarcosta.augustos@gmail.com"
#     res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
#     if(res == 1):
#         msg = "Mail Sent"
#     else:
#         msg = "Mail could not sent"
#     return HttpResponse(msg)