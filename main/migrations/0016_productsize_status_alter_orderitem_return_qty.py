# Generated by Django 5.0.1 on 2024-07-25 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_orderitem_return_qty_alter_payment_payment_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsize',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='return_qty',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Qaytarilgan tovar miqdori'),
        ),
    ]
