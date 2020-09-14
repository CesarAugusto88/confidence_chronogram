from django import forms

from apps.confidencechronograms.models import Cliente, Funcionario


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