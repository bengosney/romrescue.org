# Generated by Django 3.2.7 on 2021-09-30 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0044_remove_dog_hold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='hold_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dogs.hold'),
        ),
    ]
