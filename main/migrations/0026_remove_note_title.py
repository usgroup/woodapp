# Generated by Django 5.0.1 on 2024-07-31 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='title',
        ),
    ]
