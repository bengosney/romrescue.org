# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-30 15:45
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_auto_20160720_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='body',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Body'),
        ),
    ]
