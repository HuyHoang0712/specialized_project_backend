# Generated by Django 5.0.1 on 2024-03-11 15:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_order_status_alter_employee_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 15, 9, 14, 698798, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transportationplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 15, 9, 14, 698798, tzinfo=datetime.timezone.utc)),
        ),
    ]
