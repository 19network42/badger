# Generated by Django 4.0.4 on 2022-05-27 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='type',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
    ]
