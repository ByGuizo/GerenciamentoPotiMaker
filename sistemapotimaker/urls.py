from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('', include('contas.urls')),
    path('inventario/', include('inventario.urls')),
    path('projetos/', include('projetos.urls')),
    path('escala/', include('escala.urls')),
]
