# Generated by Django 4.2.4 on 2023-10-19 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_distances_edited_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='distances',
            name='edited_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
