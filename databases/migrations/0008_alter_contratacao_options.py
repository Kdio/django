# Generated by Django 4.0.1 on 2022-01-07 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_contratacao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contratacao',
            options={'ordering': ['associado__nome', '-ativa', 'contrato__nome', 'descricao'], 'verbose_name': 'Contratação', 'verbose_name_plural': 'Contratações'},
        ),
    ]