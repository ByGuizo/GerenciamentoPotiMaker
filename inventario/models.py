from django.db import models


class Item(models.Model):
    class Categoria(models.TextChoices):
        ELETRONICO = 'ELETRONICO', 'Eletrônico'
        FERRAMENTA = 'FERRAMENTA', 'Ferramenta'
        CONSUMIVEL = 'CONSUMIVEL', 'Consumível'
        EQUIPAMENTO = 'EQUIPAMENTO', 'Equipamento'

    class Status(models.TextChoices):
        DISPONIVEL = 'DISPONIVEL', 'Disponível'
        EM_USO = 'EM_USO', 'Em uso'
        MANUTENCAO = 'MANUTENCAO', 'Manutenção'

    nome = models.CharField('nome', max_length=120)
    categoria = models.CharField('categoria', max_length=11, choices=Categoria.choices)
    quantidade = models.PositiveIntegerField('quantidade', default=1)
    status = models.CharField('status', max_length=10, choices=Status.choices, default=Status.DISPONIVEL)

    class Meta:
        ordering = ['nome']
        verbose_name = 'item'
        verbose_name_plural = 'itens'

    def __str__(self):
        return self.nome
