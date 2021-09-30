# Generated by Django 3.2.7 on 2021-09-30 12:32

from django.db import migrations


def swap_hold(apps, schema_editor):
    Dog = apps.get_model("dogs", "Dog")
    Hold = apps.get_model("dogs", "Hold")

    medical = Hold.objects.all()[0]
    
    dogs = Dog.objects.raw("SELECT * FROM dogs_dog WHERE hold = true")
    for dog in dogs:
        dog.hold_type = medical
        dog.save()

class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0043_dog_hold_type'),
    ]

    operations = [
        migrations.RunPython(swap_hold),
        migrations.RemoveField(
            model_name='dog',
            name='hold',
        ),
    ]
