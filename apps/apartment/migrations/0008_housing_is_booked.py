# Generated by Django 5.1 on 2024-09-09 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0007_alter_housing_options'),
        ('booking', '0002_booking_booking_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='housing',
            name='is_booked',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='is_booked', to='booking.booking'),
        ),
    ]
