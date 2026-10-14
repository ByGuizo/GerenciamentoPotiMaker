from django.contrib import messages
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from contas.permissoes import exigir_coordenador

from .forms import AtividadeForm, ProjetoForm
from .models import Atividade, Projeto


def endereco_do_quadro(projeto_id):
    endereco = reverse('quadro')
    if projeto_id.isdigit():
        endereco += f'?projeto={projeto_id}'
    return endereco


def quadro(request):
    projeto_id = request.GET.get('projeto', '')
    atividades = Atividade.objects.select_related('projeto').prefetch_related('membros')
    projeto_escolhido = None
    if projeto_id.isdigit():
        projeto_escolhido = int(projeto_id)
        atividades = atividades.filter(projeto_id=projeto_escolhido)

    colunas = []
    for valor, nome in Atividade.Status.choices:
        colunas.append({'valor': valor, 'nome': nome, 'atividades': atividades.filter(status=valor)})

    contexto = {
        'colunas': colunas,
        'projetos': Projeto.objects.all(),
        'projeto_escolhido': projeto_escolhido,
    }
    return render(request, 'projetos/quadro.html', contexto)


@require_POST
def mover_atividade(request, pk, direcao):
    passos = {'avancar': 1, 'voltar': -1}
    if direcao not in passos:
        raise Http404
    atividade = get_object_or_404(Atividade, pk=pk)
    atividade.mover(passos[direcao])
    return redirect(endereco_do_quadro(request.POST.get('projeto', '')))


def nova_atividade(request):
    projeto_id = request.GET.get('projeto', '')
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save()
            messages.success(request, 'Atividade criada.')
            return redirect(endereco_do_quadro(str(atividade.projeto_id)))
    else:
        inicial = {'projeto': projeto_id} if projeto_id.isdigit() else {}
        form = AtividadeForm(initial=inicial)
    contexto = {'form': form, 'titulo': 'Nova atividade', 'voltar_url': endereco_do_quadro(projeto_id)}
    return render(request, 'formulario.html', contexto)


def editar_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada.')
            return redirect('quadro')
    else:
        form = AtividadeForm(instance=atividade)
    contexto = {'form': form, 'titulo': f'Editar {atividade}', 'voltar_url': reverse('quadro')}
    return render(request, 'formulario.html', contexto)


def excluir_atividade(request, pk):
    exigir_coordenador(request.user)
    atividade = get_object_or_404(Atividade, pk=pk)
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, f'{atividade} foi excluída.')
        return redirect('quadro')
    contexto = {'objeto': atividade, 'voltar_url': reverse('quadro')}
    return render(request, 'confirmar_exclusao.html', contexto)


def lista_projetos(request):
    projetos = Projeto.objects.annotate(total_atividades=Count('atividades'))
    return render(request, 'projetos/lista.html', {'projetos': projetos})


def novo_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto criado.')
            return redirect('lista_projetos')
    else:
        form = ProjetoForm()
    contexto = {'form': form, 'titulo': 'Novo projeto', 'voltar_url': reverse('lista_projetos')}
    return render(request, 'formulario.html', contexto)


def editar_projeto(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto atualizado.')
            return redirect('lista_projetos')
    else:
        form = ProjetoForm(instance=projeto)
    contexto = {'form': form, 'titulo': f'Editar {projeto}', 'voltar_url': reverse('lista_projetos')}
    return render(request, 'formulario.html', contexto)


def excluir_projeto(request, pk):
    exigir_coordenador(request.user)
    projeto = get_object_or_404(Projeto, pk=pk)
    if request.method == 'POST':
        projeto.delete()
        messages.success(request, f'{projeto} foi excluído.')
        return redirect('lista_projetos')
    contexto = {
        'objeto': projeto,
        'aviso': 'Todas as atividades deste projeto também serão excluídas.',
        'voltar_url': reverse('lista_projetos'),
    }
    return render(request, 'confirmar_exclusao.html', contexto)
