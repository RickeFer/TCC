# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_documento_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='ultimo_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
