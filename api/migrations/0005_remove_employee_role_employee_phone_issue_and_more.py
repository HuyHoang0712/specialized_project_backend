# Generated by Django 5.0.4 on 2024-05-03 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):


    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=254)),
                ('label', models.CharField(max_length=254)),
                ('description', models.TextField()),
                ('date_time', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'In Progress'), (2, 'Completed'), (3, 'Canceled')], default=0)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.employee')),
            ],
        ),
        migrations.CreateModel(
            name='IssueVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.issue')),
                ('vehicle_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vehicle')),
            ],
        ),
    ]
