# Generated by Django 4.2.16 on 2024-10-30 21:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0003_delete_test"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatusMessage",
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
                ("message", models.TextField()),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mini_fb.profile",
                    ),
                ),
            ],
        ),
    ]