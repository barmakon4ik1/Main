# Generated by Django 5.1.1 on 2024-09-06 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apartment", "0003_alter_housing_type"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="housing",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="housings",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
