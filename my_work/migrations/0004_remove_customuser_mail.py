# Generated by Django 4.1.5 on 2024-08-12 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0003_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='mail',
        ),
    ]
