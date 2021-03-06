# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-03-11 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20170311_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('data_adicionado', models.DateTimeField(auto_now_add=True)),
                ('ordem', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Restricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Campo')),
            ],
        ),
        migrations.CreateModel(
            name='Tabela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
                ('data_adicionado', models.DateTimeField(auto_now_add=True)),
                ('forma_normal', models.PositiveSmallIntegerField(default=0)),
                ('tabela_tipo', models.PositiveSmallIntegerField(default=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='chaveestrangeira',
            name='campo',
        ),
        migrations.RemoveField(
            model_name='chaveestrangeira',
            name='tabela',
        ),
        migrations.RemoveField(
            model_name='field',
            name='table',
        ),
        migrations.RemoveField(
            model_name='table',
            name='document',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='date_added',
            new_name='data_adicionado',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='name',
            new_name='nome',
        ),
        migrations.RemoveField(
            model_name='dependencia',
            name='dependente',
        ),
        migrations.AlterField(
            model_name='dependencia',
            name='campo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campo', to='app.Campo'),
        ),
        migrations.DeleteModel(
            name='ChaveEstrangeira',
        ),
        migrations.DeleteModel(
            name='Field',
        ),
        migrations.DeleteModel(
            name='Table',
        ),
        migrations.AddField(
            model_name='tabela',
            name='documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Documento'),
        ),
        migrations.AddField(
            model_name='campo',
            name='tabela',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.Tabela'),
        ),
        migrations.AddField(
            model_name='dependencia',
            name='chave',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='dependente', to='app.Campo'),
            preserve_default=False,
        ),
    ]
