# Generated by Django 4.0.4 on 2022-05-26 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_alter_mode_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='mode',
            new_name='modes',
        ),
    ]
