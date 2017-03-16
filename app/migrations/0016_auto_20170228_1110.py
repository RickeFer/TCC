# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_dependencia_chave'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dependencia',
            name='chave',
        ),
        migrations.AddField(
            model_name='dependencia',
            name='dependente',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='dependente', to='app.Field'),
            preserve_default=False,
        ),
    ]