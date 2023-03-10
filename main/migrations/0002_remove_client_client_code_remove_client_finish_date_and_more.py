# Generated by Django 4.1.7 on 2023-02-17 14:42

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="client_code",
        ),
        migrations.RemoveField(
            model_name="client",
            name="finish_date",
        ),
        migrations.RemoveField(
            model_name="client",
            name="paid",
        ),
        migrations.RemoveField(
            model_name="client",
            name="price",
        ),
        migrations.RemoveField(
            model_name="client",
            name="start_date",
        ),
        migrations.RemoveField(
            model_name="client",
            name="type",
        ),
        migrations.CreateModel(
            name="VpnKey",
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
                ("name", models.CharField(max_length=5)),
                ("time", models.DateField(blank=True, null=True)),
                ("start_date", models.DateField(auto_now_add=True)),
                (
                    "finish_date",
                    models.DateField(blank=True, default=main.models.now_plus_30),
                ),
                (
                    "mobile",
                    models.CharField(
                        choices=[("ANDROID", "android"), ("IOS", "ios")],
                        default="ANDROID",
                        max_length=10,
                    ),
                ),
                ("price", models.IntegerField(default=150)),
                ("paid", models.BooleanField(default=False)),
                ("locked", models.BooleanField(default=False)),
                (
                    "client",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.client",
                    ),
                ),
            ],
        ),
    ]
