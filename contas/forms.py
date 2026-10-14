from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.cache import cache

from .models import Usuario

LIMITE_DE_TENTATIVAS = 5
MINUTOS_DE_BLOQUEIO = 15


class LoginForm(AuthenticationForm):
    def chave_das_tentativas(self):
        usuario = self.data.get('username', '').lower()
        ip = self.request.META.get('HTTP_X_REAL_IP') or self.request.META.get('REMOTE_ADDR')
        return f'login-{usuario}-{ip}'

    def clean(self):
        chave = self.chave_das_tentativas()
        erros = cache.get(chave, 0)
        if erros >= LIMITE_DE_TENTATIVAS:
            raise forms.ValidationError(
                f'Muitas tentativas erradas. Espere {MINUTOS_DE_BLOQUEIO} minutos e tente de novo.'
            )
        try:
            dados = super().clean()
        except forms.ValidationError:
            cache.set(chave, erros + 1, MINUTOS_DE_BLOQUEIO * 60)
            raise
        cache.delete(chave)
        return dados

    def get_invalid_login_error(self):
        nome = self.cleaned_data.get('username')
        senha = self.cleaned_data.get('password')
        usuario = Usuario.objects.filter(username__iexact=nome).first()
        if usuario and not usuario.is_active and usuario.check_password(senha):
            return forms.ValidationError('Seu cadastro ainda está aguardando a aprovação do coordenador.')
        return super().get_invalid_login_error()


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
