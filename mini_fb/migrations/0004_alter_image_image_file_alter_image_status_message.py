# Generated by Django 4.2.16 on 2024-10-21 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0003_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image_file",
            field=models.ImageField(upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="image",
            name="status_message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="mini_fb.statusmessage"
            ),
        ),
    ]