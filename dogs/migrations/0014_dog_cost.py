# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-14 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0013_remove_dog_leash_of_life'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='cost',
            field=models.FloatField(default=240),
        ),
    ]
