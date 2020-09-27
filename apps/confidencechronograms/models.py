from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string


class ChronogramManager(models.Manager):
	# usar search()
	def search(self, query):
		# return self.get_queryset().all()
		# busca com logico E. por padrão vírgula ',' é E
		# return elf.get_queryset().filter(
		#	name__icontains=query, description__icontains=query)
		# busca OU
		return self.get_queryset().filter(
			models.Q(construction__icontains=query) | \
			models.Q(owner__icontains=query))


class Funcionario(models.Model):
    """ Tabela para cadastro com as informações do funcionário."""
    nome = models.CharField(max_length=60)
    cpf = models.CharField(blank=True, null=True, max_length=20)
    rg = models.CharField(blank=True, null=True, max_length=20)
    dt_nascimento = models.DateTimeField(verbose_name = 'Data de Nascimento', blank=True, null=True)
    sexo = models.CharField(blank=True, null=True, max_length=9)
    nacionalidade = models.CharField(blank=True, null=True, max_length=30)
    naturalidade = models.CharField(blank=True, null=True, max_length=30)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    estado_civil = models.CharField(verbose_name = 'Estado Civil', blank=True, null=True, max_length=15)
    endereco = models.CharField(verbose_name = 'Endereço', max_length=60)
    complemento = models.CharField(blank=True, null=True, max_length=30)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    cep = models.CharField(blank=True, null=True, max_length=9)
    uf = models.CharField(blank=True, null=True, max_length=2)
    email = models.EmailField(blank=True, null=True, max_length=60)
    senha = models.CharField(blank=True, null=True, max_length=16)
    fone1 = models.CharField(verbose_name = 'Telefone 1', max_length=16)
    fone2 = models.CharField(verbose_name = 'Telefone 2', blank=True, null=True, max_length=20)
    dt_admissao = models.DateTimeField(verbose_name = 'Data de Admissão', blank=True, null=True)
    cargo = models.CharField(blank=True, null=True, max_length=20)
    salario = models.FloatField(blank=True, null=True)
    bloqueado= models.CharField(max_length=3)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario_fun = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p modificar nomes para plural
    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        #ordenar
        ordering = ['nome']


    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome


class Cliente(models.Model):
    """ Tabela para cadastro com as informações do cliente."""
    nome = models.CharField(max_length=60)
    razao_social = models.CharField(verbose_name = 'Razão Social', max_length=60)
    tipo_pessoa = models.CharField(verbose_name = 'Tipo de Pessoa', max_length=8)
    cpf_cnpj = models.CharField(verbose_name = 'CPF/CNPJ', max_length=14)
    rg_ie = models.CharField(verbose_name = 'RG/IE', max_length=20)
    dt_nascimento = models.DateTimeField(verbose_name = 'Data de Nascimento', blank=True, null=True)
    sexo = models.CharField(blank=True, null=True, max_length=9)
    nacionalidade = models.CharField(blank=True, null=True, max_length=30)
    naturalidade = models.CharField(blank=True, null=True, max_length=30)
    profissao = models.CharField(blank=True, null=True, max_length=100)
    estado_civil = models.CharField(verbose_name = 'Estado Civil', blank=True, null=True, max_length=15)
    endereco = models.CharField(verbose_name = 'Endereço', max_length=60)
    complemento = models.CharField(blank=True, null=True, max_length=30)
    bairro = models.CharField(blank=True, null=True, max_length=30)
    cidade = models.CharField(blank=True, null=True, max_length=30)
    cep = models.CharField(max_length=9)
    uf = models.CharField(max_length=2)
    email = models.EmailField(max_length=60)
    email2 = models.EmailField(blank=True, null=True, max_length=60)
    senha = models.CharField(blank=True, null=True, max_length=16)
    fone1 = models.CharField(verbose_name = 'Telefone 1', max_length=16)
    fone2 = models.CharField(verbose_name = 'Telefone 2', blank=True, null=True, max_length=20)
    valor_permitido = models.FloatField(verbose_name = 'Valor Permitido', blank=True, null=True)
    dias_vencimento = models.CharField(verbose_name = 'Dias de Vencimento', blank=True, null=True, max_length=8)
    fax = models.CharField(blank=True, null=True, max_length=16)
    bloqueado= models.CharField(blank=True, null=True, max_length=3)
    # Funcionário que cadastrou como chave estrangeira (E aparecer o funcionário que está logado)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.PROTECT, blank=True, null=True)
    banco = models.IntegerField(blank=True, null=True)
    agencia = models.CharField(blank=True, null=True, max_length=10)
    conta = models.CharField(blank=True, null=True, max_length=16)
    valor_debito = models.FloatField(verbose_name = 'Valor de Débito', blank=True, null=True)
    dia_debito = models.DateTimeField(verbose_name = 'Dia do Débito', blank=True, null=True)
    dia_venc = models.DateTimeField(verbose_name = 'Dia do Vencimento', blank=True, null=True)
    senha = models.CharField(blank=True, null=True, max_length=6)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario_cli = models.ForeignKey(User, on_delete=models.CASCADE)

    # classe Meta serve p modificar nomes para plural
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #ordenar
        ordering = ['nome']


    def __str__(self):
        """ Devolve uma representação em string do modelo."""
        return self.nome

# Criar Foreinkey de Cliente ou tabém com funcionário...
class Chronogram(models.Model):
    """ Um cronograma da obra em que o cliente e
       a empresa vão poder visualizar."""
    
    construction = models.CharField(verbose_name = 'Tipo de Estrutura', max_length=200) # (verbose_name = ' Tipo de Estrutura')
    # cliente como chave estrangeira (E aparecer o cliente que já está cadastrado)
    client = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    owner = models.CharField(verbose_name = 'Proprietário',max_length=80)
    address = models.CharField(verbose_name = 'Endereço', max_length=200)
    total_time = models.CharField(verbose_name = 'Tempo total', max_length=30)
    total_price = models.DecimalField(verbose_name = 'Valor total', max_digits=10, decimal_places=4)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)


    # classe Meta serve para modificar nomes para plural
    class Meta:
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        #ordenar
        ordering = ['date_added']
    
    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return f"Cliente:{self.client}, Construção:{self.construction} " \
               f"Endereço:{self.address}, Valor:{self.total_price}"

    def get_date_chronogram(self):

        return self.date_added.strftime('%d/%m/%Y %H h : %M min')


# UM CRONOGRAMA TEM VÁRIAS TAREFAS.
class Task(models.Model):
    """Tarefa específica do cronograma."""
    ident = models.CharField(verbose_name = 'Identificador', max_length=4)
    chronogram = models.ForeignKey(Chronogram, on_delete=models.PROTECT)
    name = models.CharField(verbose_name = 'Nome', max_length=40)
    task_text = models.TextField(verbose_name = 'Descrição da Tarefa')
    start_date = models.DateField(verbose_name = 'Inicio')
    end_date = models.DateField(verbose_name = 'Termino')
    progress = models.CharField(verbose_name= 'Progresso %', max_length=3)
    dependencies = models.CharField(verbose_name='Dependências', max_length=10)
    price = models.DecimalField(verbose_name = 'Valor', max_digits=10, decimal_places=4)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)

    # classe Meta serve para modificar nomes para plural
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        #ordenar
        ordering = ['date_added']
    
    # Dicionário das tarefas
    def to_dict(self):
        """ Cria dicionário das tarefas
        
        Returns:
            dicionário -- com variáveis de Task
        """

        
        return {
            "id": self.ident,
            "name": self.name,
            "start": str(self.start_date),
            "end": str(self.end_date),
            "progress": self.progress,
            "dependencies": self.dependencies,
            "custom_class": "bar-milestone" # optional
        }

            
# {
#             "id": "3",
#             "name": "Gabaríto da Obra",
#             "start": "2020-02-24",
#             "end": "2020-03-20",
#             "progress": "20",
#             "dependencies": "2",
#             "custom_class": "bar-milestone" # optional
#         },
#
    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        data = {'tarefa': self.name}
        plain_text = render_to_string('emails/cliente.txt', data)
        html_email = render_to_string('emails/cliente.html', data)
        send_mail(
            'Tarefa cadastrada...',
            plain_text,
            'cesar@devsys.com.br',
            ['cesar@devsys.com.br', 'cesarcosta.augustos@gmail.com'],
            html_message=html_email,
            fail_silently=True, #False erro. Então, basicamente, se for verdade, você não obterá nenhum log ou erro de um e-mail enviado com falha
        )
        print(plain_text)

    def __str__(self):
        """Devolve uma representação em string do modelo."""        
        if len(self.task_text) >= 50:
            return f"{self.task_text[:50]}..."
        
        return f"{self.name} {self.task_text}"
    
# Comentario feito por um cliente
class Comentario(models.Model):
    """Tabela de comentário com referencia de cliente e funcionário."""
    dt_entrada = models.DateTimeField("Data de Entrada", auto_now=True)
    nome_cliente = models.CharField("Nome do cliente", max_length=30)
    assunto = models.CharField("Assunto", max_length=50)
    descricao = models.TextField(verbose_name = 'Descrição')
    arquivo = models.FileField(
        upload_to="chamado/arquivos/", null=True, blank=True
        )
    # referência do cliente para o funcionário dos chamados
    funcionario = models.ForeignKey(
        "Funcionario", on_delete=models.PROTECT, related_name='funcionario'
        )
    cliente = models.ForeignKey(
        "Cliente", on_delete=models.PROTECT, related_name='cliente'
        )

    #Emails
    def save(self, *args, **kwargs):
        super(Comentario, self).save(*args, **kwargs)
        data = {'cliente': self.nome_cliente}
        plain_text = render_to_string('emails/cliente_comentario.txt', data)
        html_email = render_to_string('emails/cliente_comentario.html', data)
        send_mail(
            'Chamado enviado.',
            plain_text,
            'cesar@devsys.com.br',
            ['cesar@devsys.com.br'],
            html_message=html_email,
            fail_silently=True, #False erro
        )
        print(plain_text)
    
    # classe Meta serve p modificar nomes e plural
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        # ordenar
        ordering = ["dt_entrada"]
    
    #delete
    def delete(self, *args, **kwargs):
        self.arquivo.delete()
        super().delete(*args, **kwargs)

    def get_dt_entrada_ch(self):
        """Mostra data de entrada formatada."""
        return self.dt_entrada.strftime("%d/%m/%Y %H h : %M min")

    def __str__(self):
        return f"{self.cliente.nome} {self.funcionario.nome}"
