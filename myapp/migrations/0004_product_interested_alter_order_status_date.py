# Generated by Django 4.1.2 on 2022-11-26 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_order_status_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='status_date',
            field=models.DateField(auto_now=True),
        ),
    ]
