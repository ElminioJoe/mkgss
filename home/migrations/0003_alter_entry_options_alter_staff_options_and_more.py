# Generated by Django 5.0.2 on 2024-03-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_alter_carouselimage_carousel_image_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="entry",
            options={
                "ordering": ["pk"],
                "verbose_name": "School Info Entry",
                "verbose_name_plural": "School Info Entries",
            },
        ),
        migrations.AlterModelOptions(
            name="staff",
            options={"ordering": ["pk", "role"]},
        ),
        migrations.AlterField(
            model_name="staff",
            name="role",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "---------"),
                    ("PRINCIPAL", "Principal"),
                    ("DEPUTY", "Deputy Principal"),
                    ("ADMINISTRATOR", "Administrator"),
                    ("DIRECTOR", "Board Director"),
                    ("HOD", "Head of Department"),
                    ("TEACHER", "Teacher"),
                    ("NTS", "None Teaching Staff"),
                ],
                default="",
                max_length=15,
            ),
        ),
    ]
