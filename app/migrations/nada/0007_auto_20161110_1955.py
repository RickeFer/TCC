# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-10 21:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20161110_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='order',
        ),
        migrations.RemoveField(
            model_name='field',
            name='table',
        ),
    ]