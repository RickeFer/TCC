# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-14 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20170311_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='restricao',
            name='tipo',
            field=models.CharField(choices=[('PK', 'Chave Primária'), ('FK', 'Chave Estrangeira')], default='fk', max_length=20),
            preserve_default=False,
        ),
    ]