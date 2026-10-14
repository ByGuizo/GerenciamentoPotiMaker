from datetime import time

from django.conf import settings
from django.db import models

HORARIOS = {
    'M1': (time(7, 0), time(8, 30)),
    'M2': (time(8, 50), time(10, 20)),
    'M3': (time(10, 30), time(12, 0)),
    'T1': (time(13, 0), time(14, 30)),
    'T2': (time(14, 50), time(16, 20)),
    'T3': (time(16, 30), time(18, 0)),
}


class HorarioEscala(models.Model):
    class Dia(models.IntegerChoices):
        SEGUNDA = 0, 'Segunda'
        TERCA = 1, 'Terça'
        QUARTA = 2, 'Quarta'
        QUINTA = 3, 'Quinta'
        SEXTA = 4, 'Sexta'

    class Horario(models.TextChoices):
        M1 = 'M1', 'M1 (07:00 às 08:30)'
        M2 = 'M2', 'M2 (08:50 às 10:20)'
        M3 = 'M3', 'M3 (10:30 às 12:00)'
        T1 = 'T1', 'T1 (13:00 às 14:30)'
        T2 = 'T2', 'T2 (14:50 às 16:20)'
        T3 = 'T3', 'T3 (16:30 às 18:00)'

    dia = models.IntegerField('dia', choices=Dia.choices)
    horario = models.CharField('horário', max_length=2, choices=Horario.choices)
    membros = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        limit_choices_to={'is_active': True},
        related_name='horarios_escala',
    )

    class Meta:
        ordering = ['dia', 'horario']
        verbose_name = 'horário da escala'
        verbose_name_plural = 'horários da escala'
        constraints = [
            models.UniqueConstraint(fields=['dia', 'horario'], name='um_registro_por_dia_e_horario'),
        ]

    def __str__(self):
        return f'{self.get_dia_display()}, {self.get_horario_display()}'


def horario_de_agora(agora):
    if agora.weekday() > 4:
        return None, False
    hora = agora.time()
    for codigo, (inicio, fim) in HORARIOS.items():
        if inicio <= hora < fim:
            return codigo, True
    for codigo, (inicio, fim) in HORARIOS.items():
        if hora < inicio:
            return codigo, False
    return None, False
