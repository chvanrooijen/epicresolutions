# Generated by Django 5.0.7 on 2024-12-08 20:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("resolutions", "0003_alter_role_options_alter_role_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="PDFDownloadLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("resolutions", models.ManyToManyField(to="resolutions.resolution")),
                ("roles", models.ManyToManyField(to="resolutions.role")),
            ],
        ),
    ]
