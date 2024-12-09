# Generated by Django 4.2.16 on 2024-12-09 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0003_user_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="paid_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="paid_expenses",
                to="project.user",
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="project.user"
            ),
        ),
    ]
