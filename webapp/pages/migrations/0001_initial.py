# Generated by Django 4.0.4 on 2022-06-17 15:20

from django.db import migrations, models
import django.utils.timezone
import pages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('drinks', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=100)),
                ('end', models.DateTimeField(default=pages.models.two_hours_hence)),
            ],
        ),
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=15)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
