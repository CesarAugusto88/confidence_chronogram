from django.db import models
from django.contrib.auth.models import User

class Chronogram(models.Model):
    """ Um cronograma da obra em que o cliente e
       a empresa vão poder visualizar."""
    construction = models.CharField(verbose_name = 'Tipo de Estrutura', max_length=200) # (verbose_name = ' Tipo de Estrutura')
    client = models.CharField(verbose_name = 'Cliente', max_length=80)
    owner = models.CharField(max_length=80)
    address = models.CharField(verbose_name = 'Endereço', max_length=200)
    total_time = models.CharField(verbose_name = 'Tempo total', max_length=30)
    total_price = models.CharField(verbose_name = 'Valor total', max_length=20)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return f"{self.construction}{self.client}{self.owner}"\
               f"{self.address}{self.total_time}{self.total_price}"

    def get_date_chronogram(self):

        return self.date_added.strftime('%d-%m-%Y')


# UM CRONOGRAMA TEM VÁRIAS TAREFAS.
class Task(models.Model):
    """Tarefa específica do cronograma."""
    chronogram = models.ForeignKey(Chronogram, on_delete=models.PROTECT)
    task_text = models.TextField(verbose_name = 'Dscrição da Tarefa')
    price = models.CharField(verbose_name = 'Valor', max_length=20)
    start_date = models.CharField(verbose_name = 'Inicio', max_length=10)
    end_date = models.CharField(verbose_name = 'Termino', max_length=10)
    duration = models.CharField(verbose_name = 'Duração', max_length=30)
    date_added = models.DateTimeField(verbose_name = 'Data de criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Task'

    def __str__(self):
        """Devolve uma representação em string do modelo."""        
        if len(self.task_text) >= 50:
            return f"{self.task_text[:50]}..."
        
        return f"{self.task_text}"
            

# Tabelas: Clientes para acessar os cronogramas e as tarefas, assim como os funcioários
