# Generated by Django 5.1 on 2024-09-10 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0009_alter_housing_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='housing',
            name='is_booked',
        ),
    ]
