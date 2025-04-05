from userapp.models import *
from django.db import models

from vendor.models import Vendor
# from adminapp.models import *
# from userapp.models import User
class tbl_admin(models.Model):
    password = models.CharField(max_length=200)
    email = models.EmailField()

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    food = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

from django.db import models
from userapp.models import *
class EventPackage(models.Model):
    PACKAGE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('luxury', 'Luxury'),
    ]

    name = models.CharField(max_length=20, choices=PACKAGE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    max_guests = models.IntegerField()
    services = models.CharField(max_length=255)
    extra_services = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='event_packages/')  # ✅ Added image field

    def __str__(self):
        return f"{self.get_name_display()} Package"
from django.db import models

class EventPayment(models.Model):
    PAYMENT_METHODS = [
        ("googlepay", "Google Pay"),
        ("card", "card"),
    ]

    booking = models.ForeignKey("userapp.Booking", on_delete=models.CASCADE, related_name="payments")  # String reference
    user = models.ForeignKey("userapp.User", on_delete=models.CASCADE, related_name="event_payments")
  # String reference
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    # Fields for Google Pay (UPI)
    upi_id = models.CharField(max_length=100, blank=True, null=True)

    # Fields for Card Payment
    card_number = models.CharField(max_length=16, blank=True, null=True)
    cardholder_name = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)  # Format: MM/YY
    cvv_number = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.amount_paid}"

# class VendorFeedback(models.Model):
#     vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE, related_name="feedbacks")  
#     text = models.TextField()
#     rating = models.PositiveSmallIntegerField()  # Assuming rating is from 1 to 5
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback for {self.vendor.name} - Rating: {self.rating}"