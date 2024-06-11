# Generated by Django 4.2 on 2024-05-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0005_organisationtype_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='firstName',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='lastName',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
