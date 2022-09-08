# Generated by Django 4.0.4 on 2022-07-01 12:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import events.models


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
                ('name', models.CharField(max_length=100)),
                ('end', models.DateTimeField(default=events.models.two_hours_hence)),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='events.event')),
            ],
        ),
    ]
