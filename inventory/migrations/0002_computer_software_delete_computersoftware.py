# Generated by Django 5.0.1 on 2024-02-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="computer",
            name="software",
            field=models.ManyToManyField(to="inventory.software"),
        ),
        migrations.DeleteModel(name="ComputerSoftware",),
    ]