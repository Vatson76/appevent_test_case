# Generated by Django 3.2.13 on 2022-04-17 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='google_token',
        ),
    ]
