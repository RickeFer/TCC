# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-06 13:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20161105_1908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='constraint',
        ),
        migrations.AddField(
            model_name='field',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]
