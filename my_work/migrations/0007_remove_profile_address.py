# Generated by Django 4.1.5 on 2024-08-12 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0006_profile_adhar_profile_current_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
    ]
