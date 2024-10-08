# Generated by Django 5.0.1 on 2024-07-20 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_expense_expense_summa'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_summa',
            field=models.PositiveIntegerField(default=1, verbose_name="To'langan summa"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pro_items', to='main.product', verbose_name='Mahsulot'),
        ),
    ]
