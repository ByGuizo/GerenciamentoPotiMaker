from django.urls import path

from . import views

urlpatterns = [
    path('', views.grade, name='grade'),
    path('<int:dia>/<str:horario>/', views.editar_horario, name='editar_horario'),
]
