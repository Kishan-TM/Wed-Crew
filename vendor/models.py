from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Vendor(models.Model):
    CATEGORY_CHOICES = [
        ('Photography', 'Photography'),
        ('Venue Coordinator', 'Venue Coordinator'),
        ('Decor Coordinator', 'Decor Coordinator'),
        ('Beautician', 'Beautician'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=15)
    mobile_no = models.CharField(max_length=15, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending') 

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.get_status_display()}"


from django.db import models

class Service(models.Model):
    service_name = models.CharField(max_length=200)
    details = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="services")  # ✅ Corrected reference
    image = models.ImageField(
    upload_to='service_images/',
    null=True,
    blank=True,
    default='vendor_images/decor2_MSl3hpJ.jpg'
)
   # ✅ Allows optional images

    def __str__(self):
        return self.service_name


class Vendor_addShop(models.Model):
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE, related_name="shops")  
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)
    year_in_business = models.PositiveIntegerField()
    shop_image = models.ImageField(upload_to='shop_images/')
    def __str__(self):
        return f"{self.name} - {self.year_in_business} years"


class Vendor_ShopImage(models.Model):
    shop = models.ForeignKey(Vendor_addShop, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vendor_shop_images/')

    def __str__(self):
        return f"Image for {self.shop.name}"
    
from django.conf import settings
from django.db import models


class tbl_sevice_booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="service_bookings",
        null=True,  # Allow NULL values
        blank=True  # Allow empty values
    )
    service = models.ForeignKey("Service", on_delete=models.CASCADE, related_name="service_bookings")
    advanced_price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField()
    date= models.DateField(null=True, blank=True)
    address = models.TextField()

    def __str__(self):
        return f"Booking for {self.service.service_name} at {self.time}"


from django.db import models
from django.conf import settings

class servicebooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('booked', 'Booked'),
        ('confirm', 'Confirm'),
        ('rejected','Rejected'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="bookings_of_service",
        null=True,  # Allow NULL values
        blank=True  # Allow empty values
    )
    service = models.ForeignKey("Service", on_delete=models.CASCADE, related_name="booking_of_services")
    vendor = models.ForeignKey("Vendor", on_delete=models.CASCADE)
    advanced_price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.TimeField()
    date = models.DateField(null=True, blank=True)  # Allows NULL if not provided
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')

    def __str__(self):
        return f"Booking for {self.service.service_name} at {self.time}"



from userapp.models import *
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("googlepay", "Google Pay"),
        ("card", "Credit/Debit Card"),
    ]
    
    booking = models.ForeignKey(servicebooking, on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey("userapp.User", on_delete=models.CASCADE, related_name="vendor_payments")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

 
    upi_id = models.CharField(max_length=50, blank=True, null=True)  # Only for Google Pay

    card_number = models.CharField(max_length=16, blank=True, null=True)  
    cardholder_name = models.CharField(max_length=255, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)  
    cvv_number = models.CharField(max_length=3, blank=True, null=True)  
    def __str__(self):
        return f"Payment by {self.user.name} for Booking {self.booking.id} via {self.payment_method}"
    
class UserFeedback(models.Model):
    user = models.ForeignKey("userapp.User", on_delete=models.CASCADE, related_name="feedbacks")  
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
class VendorFeedback(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)  
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)



