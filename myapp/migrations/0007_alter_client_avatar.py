# Generated by Django 4.0.5 on 2022-11-27 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_rename_image_client_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(upload_to='images'),
        ),
    ]
