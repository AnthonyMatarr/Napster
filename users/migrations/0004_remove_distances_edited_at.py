# Generated by Django 4.2.4 on 2023-10-19 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_locations_distances'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distances',
            name='edited_at',
        ),
    ]
