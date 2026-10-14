from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120, verbose_name='nome')),
                ('categoria', models.CharField(choices=[('ELETRONICO', 'Eletrônico'), ('FERRAMENTA', 'Ferramenta'), ('CONSUMIVEL', 'Consumível'), ('EQUIPAMENTO', 'Equipamento')], max_length=11, verbose_name='categoria')),
                ('quantidade', models.PositiveIntegerField(default=1, verbose_name='quantidade')),
                ('status', models.CharField(choices=[('DISPONIVEL', 'Disponível'), ('EM_USO', 'Em uso'), ('MANUTENCAO', 'Manutenção')], default='DISPONIVEL', max_length=10, verbose_name='status')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'itens',
                'ordering': ['nome'],
            },
        ),
    ]
