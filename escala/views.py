from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from contas.permissoes import exigir_coordenador

from .forms import EscalaForm
from .models import HorarioEscala, horario_de_agora


def grade(request):
    registros = HorarioEscala.objects.prefetch_related('membros')
    mapa = {(registro.dia, registro.horario): registro for registro in registros}

    agora = timezone.localtime()
    hoje = agora.weekday()
    codigo_agora, em_andamento = horario_de_agora(agora)

    dias = []
    for valor, nome in HorarioEscala.Dia.choices:
        dias.append({'valor': valor, 'nome': nome, 'hoje': valor == hoje, 'celulas': []})

    linhas = []
    for horario, rotulo in HorarioEscala.Horario.choices:
        celulas = []
        for dia in dias:
            registro = mapa.get((dia['valor'], horario))
            membros = registro.membros.all() if registro else []
            e_agora = em_andamento and dia['hoje'] and horario == codigo_agora
            celula = {'dia': dia['valor'], 'horario': horario, 'rotulo': rotulo, 'membros': membros, 'agora': e_agora}
            celulas.append(celula)
            dia['celulas'].append(celula)
        linhas.append({'rotulo': rotulo, 'celulas': celulas})

    contexto = {'dias': dias, 'linhas': linhas}
    return render(request, 'escala/grade.html', contexto)


def editar_horario(request, dia, horario):
    exigir_coordenador(request.user)
    if dia not in HorarioEscala.Dia.values or horario not in HorarioEscala.Horario.values:
        raise Http404
    registro = HorarioEscala.objects.filter(dia=dia, horario=horario).first()
    if registro is None:
        registro = HorarioEscala(dia=dia, horario=horario)

    if request.method == 'POST':
        form = EscalaForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, f'Escala de {registro} atualizada.')
            return redirect('grade')
    else:
        form = EscalaForm(instance=registro)
    contexto = {'form': form, 'titulo': str(registro), 'voltar_url': reverse('grade')}
    return render(request, 'formulario.html', contexto)
