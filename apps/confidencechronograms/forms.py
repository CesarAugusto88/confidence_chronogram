from django import forms

from apps.confidencechronograms.models import Cliente, Funcionario, Task, Chronogram,Comentario


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'nome', 'endereco', 'razao_social', 'tipo_pessoa', 'cpf_cnpj', 'rg_ie',
            'cep', 'uf', 'email', 'fone1', 'usuario_cli'
            )

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = (
            'nome', 'endereco', 'cpf', 'rg', 'fone1', 'bloqueado', 'usuario_fun'
            )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'ident', 'chronogram', 'name', 'task_text', 'start_date',
            'end_date', 'progress', 'dependencies', 'price'
            )

class ChronogramForm(forms.ModelForm):
    class Meta:
        model = Chronogram
        fields = ( 
            'construction', 'client', 'owner', 'address',
            'total_time', 'total_price'
            )
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('nome_cliente', 'assunto', 'descricao', 'arquivo', 'funcionario')