# Generated by Django 4.2.7 on 2024-03-12 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_customer_remove_hasnotification_employee_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_point', to='api.customer'),
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_point',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pickup_point', to='api.customer'),
        ),
    ]
