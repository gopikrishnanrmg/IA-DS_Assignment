# Generated by Django 4.1.2 on 2022-11-27 19:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_product_interested_alter_order_status_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=100, validators=[django.core.validators.MaxValueValidator(1000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
