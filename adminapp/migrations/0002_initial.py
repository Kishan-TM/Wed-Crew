# Generated by Django 5.1.3 on 2025-03-25 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminapp', '0001_initial'),
        ('userapp', '0001_initial'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpayment',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='userapp.booking'),
        ),
        migrations.AddField(
            model_name='eventpayment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_payments', to='userapp.user'),
        ),
        migrations.AddField(
            model_name='vendorfeedback',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='vendor.vendor'),
        ),
    ]
