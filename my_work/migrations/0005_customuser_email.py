# Generated by Django 4.1.5 on 2024-08-12 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_work', '0004_remove_customuser_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
