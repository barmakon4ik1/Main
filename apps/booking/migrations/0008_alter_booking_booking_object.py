# Generated by Django 5.1.1 on 2024-09-13 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0011_alter_address_house_number_alter_address_street'),
        ('booking', '0007_booking_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_object',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='apartment.housing'),
        ),
    ]
