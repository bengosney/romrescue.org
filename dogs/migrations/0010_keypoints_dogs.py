# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0009_keypoints'),
    ]

    operations = [
        migrations.AddField(
            model_name='keypoints',
            name='dogs',
            field=models.ManyToManyField(to='dogs.Dog'),
        ),
    ]
