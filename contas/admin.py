from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('PotiMaker', {'fields': ('matricula', 'tipo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PotiMaker', {'fields': ('first_name', 'matricula', 'tipo')}),
    )
    list_display = ('username', 'first_name', 'matricula', 'tipo', 'is_active')
    list_filter = ('tipo', 'is_active')
    search_fields = ('username', 'first_name', 'matricula')
