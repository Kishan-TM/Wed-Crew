# Generated by Django 5.1.3 on 2025-03-25 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_payment_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebooking',
            name='vendor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor'),
            preserve_default=False,
        ),
    ]
