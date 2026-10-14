from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import CadastroForm, MembroForm
from .models import Usuario
from .permissoes import exigir_coordenador


@login_not_required
def cadastro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro enviado! Aguarde a aprovação do coordenador.')
            return redirect('login')
    else:
        form = CadastroForm()
    return render(request, 'contas/cadastro.html', {'form': form})


def membros(request):
    ativos = Usuario.objects.filter(is_active=True).order_by('first_name', 'username')
    pendentes = Usuario.objects.filter(is_active=False).order_by('date_joined')
    return render(request, 'contas/membros.html', {'ativos': ativos, 'pendentes': pendentes})


@require_POST
def aprovar_membro(request, pk):
    exigir_coordenador(request.user)
    membro = get_object_or_404(Usuario, pk=pk, is_active=False)
    membro.is_active = True
    membro.save()
    messages.success(request, f'Cadastro de {membro} aprovado.')
    return redirect('membros')


def editar_membro(request, pk):
    exigir_coordenador(request.user)
    membro = get_object_or_404(Usuario, pk=pk, is_active=True)
    if request.method == 'POST':
        form = MembroForm(request.POST, instance=membro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro atualizado.')
            return redirect('membros')
    else:
        form = MembroForm(instance=membro)
    contexto = {'form': form, 'titulo': f'Editar {membro}', 'voltar_url': reverse('membros')}
    return render(request, 'formulario.html', contexto)


def senha_membro(request, pk):
    exigir_coordenador(request.user)
    membro = get_object_or_404(Usuario, pk=pk, is_active=True)
    if request.method == 'POST':
        form = SetPasswordForm(membro, request.POST)
        if form.is_valid():
            form.save()
            if membro == request.user:
                update_session_auth_hash(request, membro)
            messages.success(request, f'Senha de {membro} alterada.')
            return redirect('membros')
    else:
        form = SetPasswordForm(membro)
    contexto = {'form': form, 'titulo': f'Nova senha para {membro}', 'voltar_url': reverse('membros')}
    return render(request, 'formulario.html', contexto)


def excluir_membro(request, pk):
    exigir_coordenador(request.user)
    membro = get_object_or_404(Usuario, pk=pk)
    if membro == request.user:
        messages.error(request, 'Você não pode excluir a sua própria conta.')
        return redirect('membros')
    if membro.e_ultimo_coordenador():
        messages.error(request, 'Não é possível excluir o último coordenador.')
        return redirect('membros')
    if request.method == 'POST':
        membro.delete()
        messages.success(request, f'{membro} foi excluído do sistema.')
        return redirect('membros')
    contexto = {'objeto': membro, 'voltar_url': reverse('membros')}
    return render(request, 'confirmar_exclusao.html', contexto)
