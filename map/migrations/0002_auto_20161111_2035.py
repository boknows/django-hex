# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-11-11 20:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='gamelog',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2016, 11, 11, 20, 35, 26, 9723, tzinfo=utc), null=True),
        ),
    ]
