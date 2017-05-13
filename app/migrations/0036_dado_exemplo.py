# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-13 00:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_remove_campo_ordem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dado_Exemplo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dado', models.CharField(max_length=25)),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Campo')),
            ],
        ),
    ]