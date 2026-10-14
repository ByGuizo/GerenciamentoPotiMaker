from django.shortcuts import render
from django.utils import timezone

from contas.models import Usuario
from escala.models import HorarioEscala, horario_de_agora


def inicio(request):
    agora = timezone.localtime()
    codigo, em_andamento = horario_de_agora(agora)

    escalados = []
    rotulo_do_horario = ''
    if codigo:
        rotulo_do_horario = HorarioEscala.Horario(codigo).label
        registro = HorarioEscala.objects.filter(dia=agora.weekday(), horario=codigo).first()
        if registro:
            escalados = registro.membros.all()

    pendentes = 0
    if request.user.e_coordenador:
        pendentes = Usuario.objects.filter(is_active=False).count()

    contexto = {
        'codigo': codigo,
        'em_andamento': em_andamento,
        'rotulo_do_horario': rotulo_do_horario,
        'escalados': escalados,
        'pendentes': pendentes,
    }
    return render(request, 'inicio.html', contexto)
