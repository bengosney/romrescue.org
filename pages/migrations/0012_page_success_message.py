# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 15:32
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20160715_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='success_message',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Success Message'),
        ),
    ]
