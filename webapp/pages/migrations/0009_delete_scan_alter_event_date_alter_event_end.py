# Generated by Django 4.0.4 on 2022-05-26 12:14

from django.db import migrations, models
import django.utils.timezone
import pages.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_alter_event_date_alter_event_end'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Scan',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(default=pages.models.two_hours_hence),
        ),
    ]
