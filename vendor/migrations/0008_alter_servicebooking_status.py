# Generated by Django 5.1.3 on 2025-03-26 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_servicebooking_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicebooking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('booked', 'Booked'), ('confirm', 'Confirm'), ('rejected', 'Rejected')], default='booked', max_length=20),
        ),
    ]
