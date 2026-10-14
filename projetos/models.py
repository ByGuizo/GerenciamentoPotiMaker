from django.conf import settings
from django.db import models


class Projeto(models.Model):
    nome = models.CharField('nome', max_length=150)
    descricao = models.TextField('descrição', blank=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    class Status(models.TextChoices):
        A_FAZER = 'A_FAZER', 'A fazer'
        FAZENDO = 'FAZENDO', 'Fazendo'
        CONCLUIDO = 'CONCLUIDO', 'Concluído'

    class Prioridade(models.IntegerChoices):
        ALTA = 1, 'Alta'
        MEDIA = 2, 'Média'
        BAIXA = 3, 'Baixa'

    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='atividades')
    nome = models.CharField('nome', max_length=150)
    descricao = models.TextField('descrição', blank=True)
    status = models.CharField('status', max_length=10, choices=Status.choices, default=Status.A_FAZER)
    prioridade = models.IntegerField('prioridade', choices=Prioridade.choices, default=Prioridade.MEDIA)
    prazo = models.DateField('prazo', null=True, blank=True)
    membros = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        limit_choices_to={'is_active': True},
        related_name='atividades',
    )

    class Meta:
        ordering = ['prioridade', 'prazo']

    def __str__(self):
        return self.nome

    def mover(self, passo):
        ordem = [self.Status.A_FAZER, self.Status.FAZENDO, self.Status.CONCLUIDO]
        nova_posicao = ordem.index(self.status) + passo
        if 0 <= nova_posicao < len(ordem):
            self.status = ordem[nova_posicao]
            self.save()
