# Generated by Django 4.2.4 on 2023-10-19 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_distances_edited_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locations',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='locations',
            name='edited_at',
        ),
    ]
