# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-25 22:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_auto_20170512_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dependencia',
            name='campo',
        ),
        migrations.RemoveField(
            model_name='dependencia',
            name='chave',
        ),
        migrations.DeleteModel(
            name='Dependencia',
        ),
    ]
