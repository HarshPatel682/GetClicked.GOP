# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-27 00:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clickerapp', '0002_auto_20171119_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='section',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clickerapp.Section'),
        ),
    ]
