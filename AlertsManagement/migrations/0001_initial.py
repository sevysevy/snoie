# Generated by Django 4.2 on 2024-01-13 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('_shared', '0001_initial'),
        ('UserManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertCanal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_order', models.CharField(max_length=255)),
                ('declaration', models.TextField()),
                ('date_alert', models.DateTimeField()),
                ('village', models.CharField(max_length=255)),
                ('informant_phone', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('alert_canal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AlertsManagement.alertcanal')),
                ('arrondissement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='_shared.arrondissement')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='_shared.department')),
                ('organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagement.organisation')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='_shared.region')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagement.userprofile')),
            ],
        ),
    ]
