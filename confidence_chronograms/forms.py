 
from django import forms

from .models import Funcionario, Cliente, Chronogram, Task


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ('nome', 'dt_nascimento', 'endereco', 'cep', 'uf', 'email',
         'fone1', 'usuario_fun')
         
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nome', 'razao_social', 'tipo_pessoa', 'cpf_cnpj', 'rg_ie', 'dt_nascimento', 'endereco', 'cep', 'uf', 'email', 'fone1', 'usuario_cli')

class ChronogramForm(forms.ModelForm):
    class Meta:
        model = Chronogram
        fields = ('construction', 'client', 'owner', 'address',
        'total_time', 'total_price', 'date_added', 'usuario')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('ident', 'chronogram', 'name', 'task_text', 'start_date', 'duration', 
        'end_date', 'progress', 'dependencies', 'price', 'date_added')