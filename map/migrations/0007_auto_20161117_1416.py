# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-17 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0006_auto_20161113_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
