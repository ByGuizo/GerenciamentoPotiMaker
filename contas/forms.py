import logging

from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .limites import ip_do_cliente, limite_atingido, registrar_tentativa, zerar_tentativas
from .models import Usuario

LIMITE_DE_TENTATIVAS = 10
MINUTOS_DE_BLOQUEIO = 5

log = logging.getLogger('potimaker')


class LoginForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'inactive': 'Seu cadastro ainda está aguardando a aprovação do coordenador.',
    }

    def chave_das_tentativas(self):
        usuario = self.data.get('username', '').lower()
        return f'login-{usuario}-{ip_do_cliente(self.request)}'

    def clean(self):
        chave = self.chave_das_tentativas()
        if limite_atingido(chave, LIMITE_DE_TENTATIVAS):
            log.warning(
                'Login bloqueado: usuario=%r ip=%s',
                self.data.get('username', ''),
                ip_do_cliente(self.request),
            )
            raise forms.ValidationError(
                f'Muitas tentativas erradas. Espere {MINUTOS_DE_BLOQUEIO} minutos e tente de novo.'
            )
        try:
            dados = super().clean()
        except forms.ValidationError:
            registrar_tentativa(chave, MINUTOS_DE_BLOQUEIO * 60)
            raise
        zerar_tentativas(chave)
        return dados


class LoginAdminForm(LoginForm, AdminAuthenticationForm):
    pass


class CadastroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ['first_name', 'username', 'matricula']
        labels = {'first_name': 'Nome completo', 'username': 'Usuário'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.is_active = False
        usuario.tipo = Usuario.Tipo.MEMBRO
        if commit:
            usuario.save()
        return usuario


class MembroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'username', 'matricula', 'tipo']
        labels = {'first_name': 'Nome completo', 'username': 'Usuário'}

    def clean_tipo(self):
        tipo = self.cleaned_data['tipo']
        if tipo != Usuario.Tipo.COORDENADOR and self.instance.e_ultimo_coordenador():
            raise forms.ValidationError(
                'Este é o último coordenador. Promova outra pessoa a coordenador antes.'
            )
        return tipo
