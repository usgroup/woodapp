# Generated by Django 5.0.1 on 2024-07-12 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('name', models.CharField(max_length=255, verbose_name='Container nomi')),
                ('come_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='ExpenseType',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('title', models.CharField(max_length=255, verbose_name='Chiqim turi')),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('product_size_x', models.FloatField(verbose_name='Eni')),
                ('product_size_y', models.FloatField(verbose_name="Bo'yi")),
                ('product_size_z', models.FloatField(verbose_name='Balandligi')),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('name', models.CharField(max_length=255, verbose_name='Ismi')),
                ('phone', models.CharField(max_length=13, verbose_name='telefon raqami')),
                ('birth_date', models.DateField(blank=True, null=True)),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('product_qty', models.IntegerField(verbose_name='Mahsulot soni / dona')),
                ('product_cube', models.FloatField(verbose_name='Mahsulot miqdori / metr kub')),
                ('come_cost', models.IntegerField(verbose_name='Kelgan narxi')),
                ('rest_cube', models.FloatField(blank=True, null=True, verbose_name='Qoldiq miqdori / metr kub')),
                ('rest_qty', models.IntegerField(blank=True, null=True, verbose_name='Qoldiq soni / dona')),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.productsize', verbose_name='Mahsulot razmeri')),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('selling_price', models.IntegerField(verbose_name='Sotilish narxi')),
                ('amount_sold', models.IntegerField(verbose_name='Sotilgan miqdori | dona')),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.productsize', verbose_name='Mahsulot razmeri')),
            ],
            bases=('main.base',),
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.base')),
                ('currency', models.IntegerField(choices=[(1, 'USD'), (2, 'UZS')], default=1)),
                ('expense_summa', models.IntegerField(verbose_name='xarajat summasi')),
                ('exchange_rate', models.IntegerField(verbose_name='Valyuta kursi')),
                ('expense_distribute', models.ManyToManyField(to='main.container', verbose_name='Containerga chiqim')),
                ('expense_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.expensetype')),
                ('workers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.worker')),
            ],
            bases=('main.base',),
        ),
    ]