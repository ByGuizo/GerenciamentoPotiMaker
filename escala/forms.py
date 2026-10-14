from django import forms

from .models import HorarioEscala


class EscalaForm(forms.ModelForm):
    class Meta:
        model = HorarioEscala
        fields = ['membros']
        labels = {'membros': 'Membros neste horário'}
        widgets = {'membros': forms.CheckboxSelectMultiple}
