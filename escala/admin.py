from django.contrib import admin

from .models import HorarioEscala


@admin.register(HorarioEscala)
class HorarioEscalaAdmin(admin.ModelAdmin):
    list_display = ('dia', 'horario')
    filter_horizontal = ('membros',)
