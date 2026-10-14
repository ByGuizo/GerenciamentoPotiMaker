from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from contas.permissoes import exigir_coordenador

from .forms import ItemForm
from .models import Item


def lista_itens(request):
    busca = request.GET.get('busca', '').strip()
    categoria = request.GET.get('categoria', '')
    status = request.GET.get('status', '')

    itens = Item.objects.all()
    if busca:
        itens = itens.filter(nome__icontains=busca)
    if categoria:
        itens = itens.filter(categoria=categoria)
    if status:
        itens = itens.filter(status=status)

    contexto = {
        'itens': itens,
        'busca': busca,
        'categoria': categoria,
        'status': status,
        'categorias': Item.Categoria.choices,
        'situacoes': Item.Status.choices,
    }
    return render(request, 'inventario/lista.html', contexto)


def novo_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item cadastrado.')
            return redirect('lista_itens')
    else:
        form = ItemForm()
    contexto = {'form': form, 'titulo': 'Novo item', 'voltar_url': reverse('lista_itens')}
    return render(request, 'formulario.html', contexto)


def editar_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado.')
            return redirect('lista_itens')
    else:
        form = ItemForm(instance=item)
    contexto = {'form': form, 'titulo': f'Editar {item}', 'voltar_url': reverse('lista_itens')}
    return render(request, 'formulario.html', contexto)


def excluir_item(request, pk):
    exigir_coordenador(request.user)
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{item} foi excluído.')
        return redirect('lista_itens')
    contexto = {'objeto': item, 'voltar_url': reverse('lista_itens')}
    return render(request, 'confirmar_exclusao.html', contexto)
