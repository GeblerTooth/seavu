# Generated by Django 5.0.1 on 2024-03-10 20:22

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Software",
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
                ("name", models.CharField(max_length=256)),
                ("company_requisite", models.BooleanField()),
                ("has_licence", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
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
                (
                    "occupation",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Full-time", "Full-time"),
                            ("Part-time", "Part-time"),
                            ("Contractor", "Contractor"),
                            ("Volunteer", "Volunteer"),
                            ("Other", "Other"),
                        ],
                        max_length=128,
                        null=True,
                    ),
                ),
                ("department", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Computer",
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
                (
                    "name",
                    models.CharField(help_text="System name or other.", max_length=15),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Active", "Active"),
                            ("Inactive", "Inactive"),
                            ("Awaiting return", "Awaiting return"),
                            ("In transit", "In transit"),
                            ("Awaiting repairs", "Awaiting repairs"),
                            ("Lost", "Lost"),
                            ("Stolen", "Stolen"),
                            ("Quarantined", "Quarantined"),
                            ("Unknown", "Unknown"),
                        ],
                        max_length=128,
                    ),
                ),
                ("make", models.CharField(max_length=256)),
                ("model", models.CharField(max_length=256)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("PC", "PC"),
                            ("Laptop", "Laptop"),
                            ("Mini PC", "Mini PC"),
                            ("SBC", "SBC"),
                            ("All-in-One PC", "All-in-One PC"),
                            ("Server", "Server"),
                            ("NAS", "NAS"),
                            ("Other", "Other"),
                        ],
                        max_length=128,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "serial_number",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("tag_number", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "date_of_purchase",
                    models.DateField(
                        blank=True, default=datetime.date.today, null=True
                    ),
                ),
                ("memory_gb", models.PositiveIntegerField(blank=True, null=True)),
                ("storage_gb", models.PositiveIntegerField(blank=True, null=True)),
                ("cores", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("clock_speed_ghz", models.FloatField(blank=True, null=True)),
                ("gpu", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "software",
                    models.ManyToManyField(blank=True, to="inventory.software"),
                ),
            ],
        ),
    ]
