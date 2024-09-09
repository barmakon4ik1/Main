# Generated by Django 5.1 on 2024-09-09 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0008_housing_is_booked'),
        ('booking', '0003_booking_is_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='apartment.housing'),
        ),
    ]
