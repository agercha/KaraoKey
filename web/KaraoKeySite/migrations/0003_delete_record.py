# Generated by Django 4.1.7 on 2023-04-19 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("KaraoKeySite", "0002_record"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Record",
        ),
    ]