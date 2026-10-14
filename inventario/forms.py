from django import forms

from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'categoria', 'quantidade', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].choices = [('', 'Escolha uma categoria')] + Item.Categoria.choices
