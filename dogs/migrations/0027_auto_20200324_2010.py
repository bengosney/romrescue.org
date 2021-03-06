# Generated by Django 2.2 on 2020-03-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0026_dogphoto_promoted'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorshipInfoLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Name')),
                ('link', models.CharField(max_length=254, verbose_name='Name')),
            ],
        ),
        migrations.AlterField(
            model_name='dog',
            name='cost',
            field=models.FloatField(default=285, verbose_name='Cost'),
        ),
        migrations.AlterField(
            model_name='dog',
            name='dogStatus',
            field=models.CharField(choices=[('looking', 'Looking for a home'), ('sponsor', 'Looking for sponsorships'), ('found', 'Found a home'), ('success', 'Success story')], default='looking', max_length=8, verbose_name='Status'),
        ),
    ]
