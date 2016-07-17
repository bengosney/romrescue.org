# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 20:53
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    replaces = [(b'pages', '0002_auto_20160615_2019'), (b'pages', '0003_remove_page_map_address'), (b'pages', '0004_auto_20160617_2226'), (b'pages', '0005_homepageheader_cropped'), (b'pages', '0006_node_is_home_page'), (b'pages', '0007_auto_20160711_2016'), (b'pages', '0008_remove_page_success_message'), (b'pages', '0009_auto_20160712_2134'), (b'pages', '0010_auto_20160715_2124'), (b'pages', '0011_auto_20160715_2208'), (b'pages', '0012_page_success_message'), (b'pages', '0013_auto_20160717_1559'), (b'pages', '0014_page_form2'), (b'pages', '0015_remove_page_form2')]

    dependencies = [
        ('pages', '0001_squashed_0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'images')),
                ('strapline', models.CharField(max_length=200, verbose_name='Strap Line')),
                ('subline', models.CharField(max_length=400, verbose_name='Sub Line')),
                ('position', models.PositiveIntegerField(default=0)),
                ('itemlink', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.node')),
                ('cropped', image_cropping.fields.ImageRatioField(b'image', '1110x624', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropped')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.AlterField(
            model_name='modulelist',
            name='module',
            field=models.CharField(choices=[(b'Adoption', 'Adoptions'), (b'Success', 'Success')], max_length=200, verbose_name='Module'),
        ),
        migrations.RemoveField(
            model_name='page',
            name='map_address',
        ),
        migrations.AlterField(
            model_name='modulelist',
            name='module',
            field=models.CharField(choices=[(b'dogs:AdoptionList', 'Adoption List'), (b'Success', 'Success')], max_length=200, verbose_name='Module'),
        ),
        migrations.AddField(
            model_name='node',
            name='is_home_page',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='forms.Form'),
        ),
        migrations.RemoveField(
            model_name='page',
            name='success_message',
        ),
        migrations.AlterField(
            model_name='page',
            name='form',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='success_message',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Success Message'),
        ),
        migrations.AlterField(
            model_name='contactsubmission',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone'),
        ),
    ]
