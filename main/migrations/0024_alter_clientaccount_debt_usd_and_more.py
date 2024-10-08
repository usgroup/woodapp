# Generated by Django 5.0.1 on 2024-07-31 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_order_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccount',
            name='debt_usd',
            field=models.FloatField(default=0, verbose_name='Qarz USD'),
        ),
        migrations.AlterField(
            model_name='clientaccount',
            name='debt_uzs',
            field=models.FloatField(default=0, verbose_name='Qarz UZS'),
        ),
        migrations.AlterField(
            model_name='order',
            name='container_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='main.container'),
        ),
    ]
