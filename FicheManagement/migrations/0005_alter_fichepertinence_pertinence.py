# Generated by Django 4.2 on 2024-05-19 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FicheManagement', '0004_alter_ficheinformation_sign_obs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichepertinence',
            name='pertinence',
            field=models.BooleanField(),
        ),
    ]
