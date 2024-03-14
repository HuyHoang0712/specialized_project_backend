# Generated by Django 4.2.7 on 2024-03-13 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.employee'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.order'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vehicle'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.warehouse'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='brand',
            field=models.CharField(blank=True, default=None, max_length=32),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.employee'),
        ),
    ]
