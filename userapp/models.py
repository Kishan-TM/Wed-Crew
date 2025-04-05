from django.db import models
from adminapp.models import *
from adminapp.models import EventPackage
from userapp.models import *
from vendor.models import *
from django.core.validators import MaxValueValidator, MinValueValidator


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=15)  
   
    def __str__(self):
        return self.name

from django.db import models
from django.db import models

class Booking(models.Model):
    user = models.ForeignKey("userapp.User", on_delete=models.CASCADE, related_name="bookings")  # String reference
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    date_of_marriage = models.DateField()
    number_of_participants = models.PositiveIntegerField()
    event_package = models.ForeignKey("adminapp.EventPackage", on_delete=models.CASCADE, related_name="bookings")  # String reference

    def __str__(self):
        return f"{self.name} - {self.date_of_marriage} ({self.event_package.name})"


