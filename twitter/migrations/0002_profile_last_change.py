# Generated by Django 4.2.16 on 2025-01-05 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_change',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
