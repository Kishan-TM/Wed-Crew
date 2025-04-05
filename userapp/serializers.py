from rest_framework import serializers
from adminapp.models import EventPackage
from vendor.models import  Payment, Service, servicebooking, UserFeedback, Vendor_addShop
from adminapp.models import EventPayment
from vendor.serializers import VendorShopImageSerializer
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
class EventPackagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = EventPackage
        fields = ['id', 'name', 'image']

    def get_image(self, obj):
        if obj.image:
            # Ensure it does NOT return a full URL
            return obj.image.url if obj.image else None  
        return None


    
class EventPackageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = EventPackage
        fields = '__all__'  
    def get_image(self, obj):
        if obj.image:
            # Ensure it does NOT return a full URL
            return obj.image.url if obj.image else None  
        return None


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'details', 'total_amount']
from rest_framework import serializers
from django.contrib.auth import get_user_model
from vendor.models import servicebooking
from vendor.models import Service

User = get_user_model()

class ServiceBookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=False)

    class Meta:
        model = servicebooking
        fields = "__all__"

    def create(self, validated_data):
        if "user" not in validated_data:
            validated_data["user"] = None  # ✅ Assign NULL if user is not provided
        return super().create(validated_data)



class usercategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
        
from rest_framework import serializers


class GooglePayPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['user', 'booking', 'amount_paid', 'payment_method', 'upi_id']
        ref_name = "UserAppGooglePayPaymentSerializer"  # <-- Explicit ref_name

    def validate(self, data):
        if data.get('payment_method') != "googlepay":
            raise serializers.ValidationError("Invalid payment method for Google Pay.")
        if not data.get('upi_id'):
            raise serializers.ValidationError("UPI ID is required for Google Pay payment.")
        return data


# ✅ Card Payment Serializer
# class CardPaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = [
#             'user', 'booking', 'amount_paid', 'payment_method', 'card_number', 
#             'cardholder_name', 'expiry_date', 'cvv_number'
#         ]
#         ref_name = "VendorCardPaymentSerializer"  # <-- Explicit ref_name

#     def validate(self, data):
#         if data.get('payment_method') != "card":
#             raise serializers.ValidationError("Invalid payment method for Card Payment.")
#         if not all([data.get('card_number'), data.get('cardholder_name'), data.get('expiry_date'), data.get('cvv_number')]):
#             raise serializers.ValidationError("All card details are required for card payment.")
#         return data

class CardPaymentSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=servicebooking.objects.all())

    class Meta:
        model = Payment
        fields = [
            "booking",
            "user",
            "payment_method",
            "amount_paid",
            "card_number",
            "cardholder_name",
            "expiry_date",
            "cvv_number",
        ]

    def validate(self, data):
        # ✅ Ensure all card details are provided
        if not data.get("card_number") or not data.get("cardholder_name") or not data.get("expiry_date") or not data.get("cvv_number"):
            raise serializers.ValidationError(
                {"card_info": "All card details are required for card payments."}
            )

        # ✅ Check that payment method is card
        if data.get("payment_method") != "card":
            raise serializers.ValidationError({"payment_method": "Invalid payment method for card."})

        return data

class eventGooglePayPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPayment
        fields = ['user', 'booking', 'amount_paid', 'payment_method', 'upi_id']
        ref_name = "UserAppGooglePayPaymentSerializer"  # <-- Explicit ref_name

    def validate(self, data):
        if data.get('payment_method') != "googlepay":
            raise serializers.ValidationError("Invalid payment method for Google Pay.")
        if not data.get('upi_id'):
            raise serializers.ValidationError("UPI ID is required for Google Pay payment.")
        return data


# ✅ Card Payment Serializer
class eventCardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPayment
        fields = [
            'user', 'booking', 'amount_paid', 'payment_method', 'card_number', 
            'cardholder_name', 'expiry_date', 'cvv_number'
        ]
        ref_name = "VendorCardPaymentSerializer"  # <-- Explicit ref_name

    def validate(self, data):
        if data.get('payment_method') != "card":
            raise serializers.ValidationError("Invalid payment method for Card Payment.")
        if not all([data.get('card_number'), data.get('cardholder_name'), data.get('expiry_date'), data.get('cvv_number')]):
            raise serializers.ValidationError("All card details are required for card payment.")
        return data

class VendoraddShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor_addShop
        fields = '__all__' 
        
class VendorServiceExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service  # Ensure this matches your actual model name
        fields = ['id','service_name' ,'details', 'total_amount', 'vendor_id']  # ✅ Added 'id'


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'
        



class ViewServiceBookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.service_name", read_only=True)  # ✅ Add service name

    class Meta:
        model = servicebooking
        fields = [
            "id",
            "service_name",  # ✅ Include service_name in response
            "advanced_price",
            "time",
            "date",
            "address",
            "status",
        ]
        
        
