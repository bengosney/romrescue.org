# Generated by Django 3.2.3 on 2021-09-30 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0045_alter_dog_hold_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dog',
            name='hold',
        ),
    ]
