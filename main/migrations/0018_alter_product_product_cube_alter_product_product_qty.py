# Generated by Django 5.0.1 on 2024-07-25 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_product_is_cut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_cube',
            field=models.FloatField(default=0, verbose_name='Mahsulot miqdori / metr kub'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_qty',
            field=models.IntegerField(default=0, verbose_name='Mahsulot soni / dona'),
        ),
    ]
