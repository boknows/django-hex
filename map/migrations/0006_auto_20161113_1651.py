# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20161111_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelog',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
