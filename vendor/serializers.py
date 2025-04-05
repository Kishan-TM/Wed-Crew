from rest_framework import serializers

from adminapp import apps
from .models import *

from userapp.models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        
class VendorShopImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # ✅ Convert image path to relative path

    class Meta:
        model = Vendor_ShopImage
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # ✅ Return only the relative path
        return None

class VendoraddShopSerializer(serializers.ModelSerializer):
    work_images = VendorShopImageSerializer(many=True, read_only=True, source="images")  # ✅ Rename images to work_images
    shop_image = serializers.SerializerMethodField()  # ✅ Convert main image to relative path

    class Meta:
        model = Vendor_addShop
        fields = ['id', 'name', 'address', 'email', 'mobile_no', 'year_in_business', 'shop_image', 'vendor', 'work_images']  # ✅ Use work_images

    def get_shop_image(self, obj):
        if obj.shop_image:
            return obj.shop_image.url  # ✅ Return only the relative path
        return None


class VendorWorkImageUpdateSerializer(serializers.Serializer):
    work_images = serializers.ListField(
        child=serializers.ImageField(), required=True
    )

    def update(self, instance, validated_data, replace):
        images = validated_data.get('work_images', [])

        if replace:
            instance.images.all().delete()  # ✅ Remove old images if PUT is used

        # ✅ Bulk create multiple images
        new_images = [Vendor_ShopImage(shop=instance, image=img) for img in images]
        Vendor_ShopImage.objects.bulk_create(new_images)  

        return instance

    
class VendorServiceExtendedSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)  # Fetch related vendor name

    class Meta:
        model = Service
        fields = ['name', 'details', 'amount', 'vendor_id', 'vendor_name']
    
class ServiceSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # ✅ Custom method to return only the relative path

    class Meta:
        model = Service
        fields = '__all__'

    def get_image(self, obj):
            if obj.image:
                return f"{obj.image.name}"
            return None

class VendorbookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = servicebooking
        fields = "__all__" 


# ✅ Google Pay Payment Serializer
class GooglePayPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "booking", "amount_paid", "payment_method", "upi_id", "payment_date"]
        extra_kwargs = {
            "payment_method": {"default": "googlepay"},
            "upi_id": {"required": True},
        }
        ref_name = "VendorGooglePayPaymentSerializer"  # <-- Explicit ref_name

    def validate(self, data):
        if data.get("payment_method") != "googlepay":
            raise serializers.ValidationError({"payment_method": "Payment method must be Google Pay."})
        if not data.get("upi_id"):
            raise serializers.ValidationError({"upi_id": "UPI ID is required for Google Pay."})
        return data

# ✅ Card Payment Serializer
class CardPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id", "user", "booking", "amount_paid", "payment_method",
            "card_number", "cardholder_name", "expiry_date", "cvv_number", "payment_date"
        ]
        extra_kwargs = {
            "payment_method": {"default": "card"},
            "card_number": {"required": True},
            "cardholder_name": {"required": True},
            "expiry_date": {"required": True},
            "cvv_number": {"required": True},
        }
        ref_name = "UserAppCardPaymentSerializer"  # <-- Explicit ref_name

    def validate(self, data):
        if data.get("payment_method") != "card":
            raise serializers.ValidationError({"payment_method": "Payment method must be Card."})
        if not data.get("card_number") or len(data.get("card_number")) != 16:
            raise serializers.ValidationError({"card_number": "Card number must be 16 digits."})
        if not data.get("cvv_number") or len(data.get("cvv_number")) != 3:
            raise serializers.ValidationError({"cvv_number": "CVV must be 3 digits."})
        return data
    
class VendorFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'
        
        

class VendorServiceBookingSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.service_name", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = servicebooking
        fields = [
            "id",
            "user_name",
            "vendor",
            "service_name",
            "advanced_price",
            "time",
            "date",
            "address",
            "status",
        ]
        
        
class VendorFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorFeedback
        fields = '__all__'