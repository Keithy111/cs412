# Generated by Django 4.2.16 on 2024-12-10 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0004_profile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories",
                to="project.profile",
            ),
            preserve_default=False,
        ),
    ]
