# Generated by Django 5.0.4 on 2024-04-20 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_schedule'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='booking',
            new_name='booked',
        ),
    ]
