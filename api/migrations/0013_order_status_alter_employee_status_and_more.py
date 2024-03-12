# Generated by Django 5.0.1 on 2024-03-11 15:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_order_date_alter_transportationplan_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 15, 7, 36, 268384, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='transportationplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 15, 7, 36, 267383, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='status',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
