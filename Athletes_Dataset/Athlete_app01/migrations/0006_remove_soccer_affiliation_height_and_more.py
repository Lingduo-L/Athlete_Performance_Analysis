# Generated by Django 4.1 on 2022-11-26 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Athlete_app01", "0005_soccer_affiliation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="soccer_affiliation",
            name="Height",
        ),
        migrations.RemoveField(
            model_name="soccer_affiliation",
            name="Weight",
        ),
    ]