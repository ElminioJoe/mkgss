# Generated by Django 5.0.2 on 2024-03-07 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_staff_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("PRINCIPAL", "Principal"),
                    ("DEPUTY", "Deputy Principal"),
                    ("ADMINISTRATIVE", "Administrative"),
                    ("BOM", "Board of Management"),
                    ("TEACHER", "Teacher"),
                    ("NTS", "None Teaching Staff"),
                ],
                default="",
                max_length=15,
            ),
        ),
    ]