# Generated by Django 5.0.7 on 2024-09-03 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resolutions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="resolution",
            name="cause",
        ),
        migrations.AddField(
            model_name="resolution",
            name="causes",
            field=models.ManyToManyField(to="resolutions.cause"),
        ),
    ]