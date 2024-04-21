# Generated by Django 5.0.4 on 2024-04-17 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialities', models.CharField(max_length=100)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='icons')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=15)),
                ('address1', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('photo_id', models.ImageField(upload_to='photo_id')),
                ('doctor_credentials', models.ImageField(upload_to='doctor_credentials')),
                ('profile_photo', models.ImageField(upload_to='profile_photo')),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(default=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('speciality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='doctor.specialities')),
            ],
        ),
    ]