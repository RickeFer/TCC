# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-05-13 02:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_dado_exemplo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dado_exemplo',
            old_name='dado',
            new_name='text',
        ),
    ]