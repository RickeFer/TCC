# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_table_type_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Field')),
            ],
        ),
    ]
