# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-26 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_auto_20160812_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='job',
            field=models.CharField(default='job', max_length=150, verbose_name='Job'),
            preserve_default=False,
        ),
    ]
