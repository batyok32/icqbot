# Generated by Django 4.1.7 on 2023-02-17 20:55

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_alter_vpnkey_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vpnkey",
            name="client",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="vpns",
                to="main.client",
            ),
        ),
        migrations.AlterField(
            model_name="vpnkey",
            name="finish_date",
            field=models.DateTimeField(blank=True, default=main.models.now_plus_30),
        ),
        migrations.AlterField(
            model_name="vpnkey",
            name="start_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
