# Generated by Django 5.0.1 on 2024-07-16 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_product_product_container'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('name', models.CharField(max_length=255, verbose_name='Ismi')),
                ('phone', models.CharField(max_length=13, verbose_name='telefon raqami')),
                ('debt_usd', models.IntegerField(default=0, verbose_name='Qarz USD')),
                ('debt_uzs', models.IntegerField(default=0, verbose_name='Qarz UZS')),
            ],
            bases=('main.base',),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='container_products', to='main.container', verbose_name='cointainer nomi'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='main.productsize', verbose_name='Mahsulot razmeri'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('currency', models.IntegerField(choices=[(1, 'USD'), (2, 'UZS')], default=2)),
                ('sale_exchange_rate', models.IntegerField(verbose_name='Valyuta kursi')),
                ('total_summa', models.PositiveIntegerField(verbose_name='Total summa')),
                ('debt_status', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.client')),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('product_cost', models.IntegerField(verbose_name='Mahsulot narxi')),
                ('amount_sold', models.IntegerField(verbose_name='Sotilgan miqdori | dona')),
                ('total_price', models.PositiveIntegerField(default=0)),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order')),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.product', verbose_name='Mahsulot')),
            ],
            bases=('main.base',),
        ),
        migrations.DeleteModel(
            name='SaleProduct',
        ),
    ]
