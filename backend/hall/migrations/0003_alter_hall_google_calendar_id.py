# Generated by Django 3.2.13 on 2022-04-17 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hall', '0002_alter_hall_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hall',
            name='google_calendar_id',
            field=models.CharField(max_length=128, verbose_name='id календаря google'),
        ),
    ]
