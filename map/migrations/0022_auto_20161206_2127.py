# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 21:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0021_action_tile_acting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_type',
            field=models.CharField(choices=[('TA', 'Tile Assignment'), ('MISC', 'Miscellaneous'), ('ATT', 'Attack'), ('PL', 'Unit Placement'), ('FORT', 'Fortify Unit'), ('BEGN', 'Begin Turn'), ('END', 'End Turn')], default='MISC', max_length=4),
        ),
    ]
