# Generated by Django 4.2.7 on 2024-03-11 14:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_order_date_alter_transportationplan_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_id', to='api.deliverypoint'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 14, 46, 36, 979747, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pickup_id', to='api.deliverypoint'),
        ),
        migrations.AlterField(
            model_name='transportationplan',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 14, 46, 36, 979747, tzinfo=datetime.timezone.utc)),
        ),
    ]
