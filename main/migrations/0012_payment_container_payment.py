# Generated by Django 5.0.1 on 2024-07-22 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='container_payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.container', verbose_name="to'lov qilingan container"),
        ),
    ]