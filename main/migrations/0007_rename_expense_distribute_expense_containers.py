# Generated by Django 5.0.1 on 2024-07-20 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_client_alter_product_product_container_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='expense_distribute',
            new_name='containers',
        ),
    ]
