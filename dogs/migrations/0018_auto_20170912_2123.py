# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-09-12 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0017_auto_20170912_2055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ('position',), 'verbose_name': 'Filter', 'verbose_name_plural': 'Filters'},
        ),
        migrations.AddField(
            model_name='filter',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
