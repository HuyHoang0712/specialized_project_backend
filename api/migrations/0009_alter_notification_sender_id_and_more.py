# Generated by Django 5.0.4 on 2024-05-24 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_message_notification_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.employee'),
        ),
        migrations.AlterField(
            model_name='notificationissue',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.issue'),
        ),
        migrations.AlterField(
            model_name='notificationorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order'),
        ),
    ]
