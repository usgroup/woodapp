# Generated by Django 5.0.1 on 2024-07-12 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_container_come_date_alter_container_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
