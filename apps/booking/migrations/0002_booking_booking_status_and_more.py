# Generated by Django 5.1 on 2024-09-09 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('PENDING', 'Pending confirmation'), ('CANCELED', 'Canceled'), ('UNCONFIRMED', 'Unconfirmed')], default='PENDING', max_length=30, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date_from',
            field=models.DateField(blank=True, null=True, verbose_name='Booking from'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date_to',
            field=models.DateField(blank=True, null=True, verbose_name='Booking to'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Booking time'),
        ),
    ]
