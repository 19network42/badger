# Generated by Django 4.0.4 on 2022-06-02 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.IntegerField(unique=True)),
                ('uid', models.CharField(blank=True, max_length=255, null=True)),
                ('reference', models.CharField(blank=True, max_length=255, null=True)),
                ('badge_type', models.CharField(choices=[('PISCINEUX', 'Piscineux'), ('STUDENT', 'Student')], default='STUDENT', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('intra_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('login', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('displayname', models.CharField(max_length=255)),
                ('image_url', models.URLField()),
                ('is_staff', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StudentBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField(blank=True, null=True)),
                ('caution_paid', models.FloatField(default=0.0)),
                ('caution_returned', models.BooleanField(default=False)),
                ('lost', models.BooleanField(default=False)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='students_badges', to='badges.badge')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='students_badges', to='badges.student')),
            ],
        ),
    ]
