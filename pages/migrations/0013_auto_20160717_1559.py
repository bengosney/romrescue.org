# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 15:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_page_success_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactsubmission',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone'),
        ),
    ]
