from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.functions import Lower


class UsuarioManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('tipo', Usuario.Tipo.COORDENADOR)
        return super().create_superuser(username, email, password, **extra_fields)


class Usuario(AbstractUser):
    class Tipo(models.TextChoices):
        COORDENADOR = 'COORDENADOR', 'Coordenador'
        MEMBRO = 'MEMBRO', 'Membro'

    matricula = models.CharField('matrícula', max_length=20, unique=True)
    tipo = models.CharField('tipo', max_length=11, choices=Tipo.choices, default=Tipo.MEMBRO)

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['matricula']

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'
        constraints = [
            models.UniqueConstraint(
                Lower('username'),
                name='username_unico_sem_maiusculas',
                violation_error_message='Já existe um usuário com esse nome.',
            ),
        ]

    @property
    def e_coordenador(self):
        return self.tipo == self.Tipo.COORDENADOR

    def e_ultimo_coordenador(self):
        outros = Usuario.objects.filter(tipo=self.Tipo.COORDENADOR, is_active=True).exclude(pk=self.pk)
        return self.e_coordenador and not outros.exists()

    def __str__(self):
        return self.get_full_name() or self.username
