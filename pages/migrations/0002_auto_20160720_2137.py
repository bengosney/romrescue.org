# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 21:37
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_extensions.db.fields
import image_cropping.fields
import polymorphic_tree.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone')),
                ('enquiry', models.TextField(verbose_name='Enquiry')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FosteringSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('contact_number', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomePageHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'images')),
                ('cropped', image_cropping.fields.ImageRatioField(b'image', '1110x624', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropped')),
                ('strapline', models.CharField(max_length=200, verbose_name='Strap Line')),
                ('subline', models.CharField(max_length=400, verbose_name='Sub Line')),
                ('position', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, b'Live'), (2, b'Draft'), (3, b'Hidden')], default=1)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('nav_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Navigation Title')),
                ('nav_icon', models.CharField(blank=True, choices=[(b'twitter', b'Twitter'), (b'facebook', b'Facebook'), (b'instagram', b'Instagram'), (b'linkedin', b'LinkedIn')], max_length=200, null=True, verbose_name='Navigation Icon')),
                ('nav_icon_only', models.BooleanField(default=False, verbose_name='Icon Only')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=b'title')),
                ('title_tag', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title Tag')),
                ('meta_description', models.TextField(blank=True, null=True)),
                ('active_url_helper', models.CharField(blank=True, max_length=255, null=True)),
                ('is_home_page', models.BooleanField()),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'verbose_name': 'Site node',
                'verbose_name_plural': 'Site nodes',
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Empty',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.node')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'verbose_name': 'Empty Item',
                'verbose_name_plural': 'Empty Items',
            },
            bases=('pages.node',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.node')),
                ('URL', models.URLField(verbose_name='URL')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'verbose_name': 'External Link',
                'verbose_name_plural': 'External Links',
            },
            bases=('pages.node',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ModuleList',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.node')),
                ('module', models.CharField(choices=[(b'dogs:AdoptionList', 'Adoption List'), (b'dogs:SuccessList', 'Success List')], max_length=200, verbose_name='Module')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Body')),
            ],
            options={
                'verbose_name': 'Module List',
                'verbose_name_plural': 'Module Lists',
            },
            bases=('pages.node',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.node')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Body')),
                ('form', models.CharField(blank=True, choices=[(b'ContactForm', b'Contact Form'), (b'FosteringForm', b'Fostering Form')], max_length=100, null=True)),
                ('success_message', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Success Message')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=('pages.node',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.node')),
                ('social', models.CharField(choices=[(b'twitter', b'Twitter'), (b'facebook', b'Facebook'), (b'instagram', b'Instagram'), (b'linkedin', b'LinkedIn')], max_length=200, verbose_name='Social Type')),
            ],
            options={
                'ordering': ('tree_id', 'lft'),
                'abstract': False,
                'verbose_name': 'Social Link',
                'verbose_name_plural': 'Social Links',
            },
            bases=('pages.node',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='parent',
            field=polymorphic_tree.models.PolymorphicTreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pages.node', verbose_name='parent'),
        ),
        migrations.AddField(
            model_name='node',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_pages.node_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='homepageheader',
            name='itemlink',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.node'),
        ),
    ]
