# Generated by Django 4.2 on 2024-01-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_shared', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrondissement',
            name='name_code',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='department',
            name='name_code',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='region',
            name='name_code',
            field=models.CharField(default='', max_length=255),
        ),
    ]
