# Generated by Django 3.0.8 on 2020-07-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_auto_20170301_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='images/team'),
        ),
    ]
