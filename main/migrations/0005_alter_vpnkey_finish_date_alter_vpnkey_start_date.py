# Generated by Django 4.1.7 on 2023-02-17 20:57

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_alter_vpnkey_client_alter_vpnkey_finish_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vpnkey",
            name="finish_date",
            field=models.DateField(blank=True, default=main.models.now_plus_30),
        ),
        migrations.AlterField(
            model_name="vpnkey",
            name="start_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
