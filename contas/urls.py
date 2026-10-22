from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path(
        'entrar/',
        auth_views.LoginView.as_view(
            template_name='contas/login.html',
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('minha-senha/', views.minha_senha, name='minha_senha'),
    path('membros/', views.membros, name='membros'),
    path('membros/<int:pk>/aprovar/', views.aprovar_membro, name='aprovar_membro'),
    path('membros/<int:pk>/editar/', views.editar_membro, name='editar_membro'),
    path('membros/<int:pk>/senha/', views.senha_membro, name='senha_membro'),
    path('membros/<int:pk>/excluir/', views.excluir_membro, name='excluir_membro'),
]
