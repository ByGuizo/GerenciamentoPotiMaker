from django import forms

from .models import Atividade, Projeto


class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['nome', 'descricao']
        widgets = {'descricao': forms.Textarea(attrs={'rows': 4})}


class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['projeto', 'nome', 'descricao', 'status', 'prioridade', 'prazo', 'membros']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'prazo': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'membros': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projeto'].empty_label = 'Escolha um projeto'
