# Generated by Django 5.0.1 on 2024-07-20 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_expense_distribute_expense_containers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='expense_summa',
            field=models.FloatField(verbose_name='xarajat summasi'),
        ),
    ]
