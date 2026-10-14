from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HorarioEscala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.IntegerField(choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta')], verbose_name='dia')),
                ('horario', models.CharField(choices=[('M1', 'M1 (07:00 às 08:30)'), ('M2', 'M2 (08:50 às 10:20)'), ('M3', 'M3 (10:30 às 12:00)'), ('T1', 'T1 (13:00 às 14:30)'), ('T2', 'T2 (14:50 às 16:20)'), ('T3', 'T3 (16:30 às 18:00)')], max_length=2, verbose_name='horário')),
                ('membros', models.ManyToManyField(blank=True, limit_choices_to={'is_active': True}, related_name='horarios_escala', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'horário da escala',
                'verbose_name_plural': 'horários da escala',
                'ordering': ['dia', 'horario'],
                'constraints': [models.UniqueConstraint(fields=('dia', 'horario'), name='um_registro_por_dia_e_horario')],
            },
        ),
    ]
