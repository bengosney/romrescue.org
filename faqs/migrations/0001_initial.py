# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseFAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=150)),
                ('answer', models.CharField(max_length=500)),
                ('position', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='AdoptionFAQ',
            fields=[
                ('basefaq_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='faqs.BaseFAQ')),
            ],
            bases=('faqs.basefaq',),
        ),
        migrations.CreateModel(
            name='FosteringFAQ',
            fields=[
                ('basefaq_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='faqs.BaseFAQ')),
            ],
            bases=('faqs.basefaq',),
        ),
    ]
