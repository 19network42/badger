# Generated by Django 4.0.4 on 2022-05-23 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_event_duration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Participant',
        ),
    ]