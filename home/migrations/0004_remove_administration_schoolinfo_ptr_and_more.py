# Generated by Django 5.0.2 on 2024-02-09 12:51

import django.db.models.deletion
import django_ckeditor_5.fields
import django_resized.forms
import home.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_schoolinfo_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="administration",
            name="schoolinfo_ptr",
        ),
        migrations.RemoveField(
            model_name="admission",
            name="schoolinfo_ptr",
        ),
        migrations.RemoveField(
            model_name="curricular",
            name="schoolinfo_ptr",
        ),
        migrations.RemoveField(
            model_name="schoolhistory",
            name="schoolinfo_ptr",
        ),
        migrations.RemoveField(
            model_name="schoolvalue",
            name="schoolinfo_ptr",
        ),
        migrations.AlterField(
            model_name="news",
            name="news",
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
        migrations.CreateModel(
            name="Entry",
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
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date Created"
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(auto_now=True, verbose_name="Date Modified"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="Deleted"),
                ),
                (
                    "date_deleted",
                    models.DateTimeField(
                        blank=True,
                        editable=False,
                        null=True,
                        verbose_name="Date Deleted",
                    ),
                ),
                (
                    "entry",
                    models.CharField(
                        blank=True,
                        choices=[
                            (None, "---------"),
                            ("ADMINISTRATION", "Administration"),
                            ("ADMISSION", "Admissions"),
                            ("ACADEMIC", "Academic"),
                            ("CURRICULAR", "Co-Curricular"),
                            ("HISTORY", "School History"),
                            ("PRINCIPLES", "Principles"),
                        ],
                        default=(None, "---------"),
                        max_length=15,
                    ),
                ),
                ("title", models.CharField(blank=True, default="", max_length=150)),
                ("content", django_ckeditor_5.fields.CKEditor5Field()),
                (
                    "cover_image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=["middle", "center"],
                        default="",
                        force_format=None,
                        keep_meta=True,
                        quality=75,
                        scale=None,
                        size=[1920, 1300],
                        upload_to="entries/",
                    ),
                ),
                (
                    "image_alt_text",
                    home.models.ImageAltTextField(
                        blank=True,
                        help_text="Optional: short description of what the image entails.",
                        max_length=255,
                    ),
                ),
                (
                    "parent_entry",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="children",
                        to="home.entry",
                        verbose_name="Parent Entry",
                    ),
                ),
            ],
            options={
                "verbose_name": "School Info Entry",
                "verbose_name_plural": "School Info Entries",
            },
        ),
        migrations.DeleteModel(
            name="Academic",
        ),
        migrations.DeleteModel(
            name="Administration",
        ),
        migrations.DeleteModel(
            name="Admission",
        ),
        migrations.DeleteModel(
            name="Curricular",
        ),
        migrations.DeleteModel(
            name="SchoolHistory",
        ),
        migrations.DeleteModel(
            name="SchoolInfo",
        ),
        migrations.DeleteModel(
            name="SchoolValue",
        ),
    ]
