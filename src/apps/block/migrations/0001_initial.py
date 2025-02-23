# Generated by Django 5.1.6 on 2025-02-13 05:18

import django.db.models.deletion
import uuid6
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("currency", "0001_initial"),
        ("provider", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Block",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid6.uuid7,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("block_number", models.BigIntegerField()),
                ("created_at", models.DateTimeField()),
                ("stored_at", models.DateTimeField(auto_now_add=True)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="currency.currency",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="provider.provider",
                    ),
                ),
            ],
            options={
                "verbose_name": "Block",
                "verbose_name_plural": "Blocks",
                "db_table": "block",
            },
        ),
    ]
