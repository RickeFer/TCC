# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-05 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_field_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='constraint',
            field=models.CharField(default='00000', max_length=5),
        ),
    ]
