import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='nome')),
                ('descricao', models.TextField(blank=True, verbose_name='descrição')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='nome')),
                ('descricao', models.TextField(blank=True, verbose_name='descrição')),
                ('status', models.CharField(choices=[('A_FAZER', 'A fazer'), ('FAZENDO', 'Fazendo'), ('CONCLUIDO', 'Concluído')], default='A_FAZER', max_length=10, verbose_name='status')),
                ('prioridade', models.IntegerField(choices=[(1, 'Alta'), (2, 'Média'), (3, 'Baixa')], default=2, verbose_name='prioridade')),
                ('prazo', models.DateField(blank=True, null=True, verbose_name='prazo')),
                ('membros', models.ManyToManyField(blank=True, limit_choices_to={'is_active': True}, related_name='atividades', to=settings.AUTH_USER_MODEL)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atividades', to='projetos.projeto')),
            ],
            options={
                'ordering': ['prioridade', 'prazo'],
            },
        ),
    ]
