# Generated by Django 5.1 on 2024-09-09 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_booking_booking_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
