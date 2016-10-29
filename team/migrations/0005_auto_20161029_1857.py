# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-29 18:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_teammember_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/teamdogs')),
                ('thumbnail', image_cropping.fields.ImageRatioField('image', '150x150', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='thumbnail')),
                ('position', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.AlterField(
            model_name='teammember',
            name='cropped',
            field=image_cropping.fields.ImageRatioField('image', '400x400', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropped'),
        ),
        migrations.AddField(
            model_name='dogphoto',
            name='TeamMember',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.TeamMember'),
        ),
    ]
