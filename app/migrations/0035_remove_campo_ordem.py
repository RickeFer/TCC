# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-07 19:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20170505_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campo',
            name='ordem',
        ),
    ]
