# Generated by Django 4.2.18 on 2025-02-13 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_api', '0003_alter_userdetails_firstname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='username',
        ),
    ]
