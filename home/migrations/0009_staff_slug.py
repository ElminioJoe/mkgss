# Generated by Django 5.0.2 on 2024-03-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0008_remove_news_news_remove_staff_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="slug",
            field=models.SlugField(
                blank=True, editable=False, max_length=500, unique=True
            ),
        ),
    ]