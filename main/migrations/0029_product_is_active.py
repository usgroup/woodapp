# Generated by Django 5.0.1 on 2024-08-22 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_productsize_product_size_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]