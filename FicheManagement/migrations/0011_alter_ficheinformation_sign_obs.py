# Generated by Django 4.2 on 2024-06-05 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FicheManagement', '0010_fichepertinence_arret_activite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficheinformation',
            name='sign_obs',
            field=models.TextField(default=''),
        ),
    ]