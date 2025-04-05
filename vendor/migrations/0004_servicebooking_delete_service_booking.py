# Generated by Django 5.1.3 on 2025-03-25 10:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_service_booking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='servicebooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advanced_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.TimeField()),
                ('date', models.DateField(blank=True, null=True)),
                ('address', models.TextField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_of_services', to='vendor.service')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings_of_service', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='service_booking',
        ),
    ]
