from urllib import request
from django.shortcuts import get_object_or_404
from jsonschema import ValidationError
from rest_framework import generics, status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.models import User
from userapp.serializers import UserSerializer
from .models import Vendor
from .serializers import VendorSerializer
from .serializers import *

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        instance = serializer.save()  
        return Response(
            {
                "status": "success",
                "message": "Vendor created successfully!",
                "vendor_id": instance.id
            },
            status=status.HTTP_200_OK
        )

from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer
from vendor.serializers import VendorSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    http_method_names = ['post']
    serializer_class = ServiceSerializer

    def post(self, request, *args, **kwargs):
        """Custom POST response for creating a new service"""
        vendor_id = request.data.get("vendor_id")  

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save() 

            return Response(
                {
                    "message": "Service created successfully",
                    "status": "success",
                    "service_id": service.id,  
                    "vendor_id": vendor_id, 
                },
                status=status.HTTP_200_OK,  
            )

        return Response(
            {
                "message": "Failed to create service",
                "status": "error",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


from rest_framework.response import Response
from rest_framework import status

def get(self, request, *args, **kwargs):
    """Custom GET response for retrieving services"""
    services = self.get_queryset()
    serializer = self.get_serializer(services, many=True)
    
    # Return the list directly instead of wrapping it inside "data"
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer
class VendorLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor = Vendor.objects.get(email=email)

            # Validate password securely
            if password==vendor.password:
                serializer = VendorSerializer(vendor)
                return Response({"message": "Login successful","vendor_id": vendor.id, "Role":"Vendor","status": vendor.status}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


class VendoraddShopListCreateView(generics.ListCreateAPIView):
    queryset = Vendor_addShop.objects.all()
    serializer_class = VendoraddShopSerializer
    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')  
        serializer = self.get_serializer(data=request.data, context={"request": request})  # ✅ Pass request context

        if serializer.is_valid():
            shop = serializer.save()
            
            for image in images:
                Vendor_ShopImage.objects.create(shop=shop, image=image)

            return Response(
                {
                    "message": "Vendor Shop added successfully!",
                    "status": "success",
                    "vendor_id": shop.vendor.id, 
                    "data": VendoraddShopSerializer(shop, context={"request": request}).data,  # ✅ Ensure request context
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class VendoraddShopRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor_addShop.objects.all()
    serializer_class = VendoraddShopSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Vendor Shop deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
class VendorServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    http_method_names = ['get', 'delete']  # ✅ Allow DELETE requests

    def list(self, request, *args, **kwargs):
        vendor_id = request.query_params.get("vendor_id")

        if not vendor_id:
            return Response({"error": "Valid vendor_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        vendor = get_object_or_404(Vendor, id=int(vendor_id))
        services = Service.objects.filter(vendor_id=vendor_id)
        services_data = self.get_serializer(services, many=True).data  

        # ✅ Format the response with vendor ID only
        formatted_services = [
            {
                "id": service["id"],
                "service_name": service["service_name"],
                "details": service["details"],
                "total_amount": service["total_amount"],
                "vendor": vendor.id
            }
            for service in services_data
        ]

        return Response(formatted_services, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        service_id = request.query_params.get("service_id")

        if not service_id:
            return Response({"error": "service_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = get_object_or_404(Service, id=int(service_id))

        service.delete()  # ✅ Delete the service

        return Response({"message": "Service deleted successfully"}, status=status.HTTP_200_OK)
class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorSerializer  
    http_method_names = ['get', 'patch', 'post']

    def get_object(self):
        vendor_id = self.request.query_params.get("vendor_id")
        if not vendor_id:
            raise ValidationError({"error": "vendor_id is required"})
        return get_object_or_404(Vendor, id=vendor_id)

    def get(self, request, *args, **kwargs):
        """Retrieve vendor details along with their services."""
        vendor = self.get_object()
        services = Service.objects.filter(vendor_id=vendor.id)
        services_data = ServiceSerializer(services, many=True).data 

        return Response({
            "vendor_id": vendor.id,
            "name": vendor.name,
            "email": vendor.email,
            "mobile_no": vendor.mobile_no,
            "category": vendor.category,
            "status": vendor.status,
            "image": vendor.image.url if vendor.image else None,  # Ensure proper image URL handling
            "services": services_data
        }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """Update vendor details partially."""
        vendor = self.get_object()
        serializer = VendorSerializer(vendor, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vendor updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ViewservicesView(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor_id')  # ✅ Corrected query param name
        print(request.query_params)
        if not vendor_id:
            return Response(
                {"status": "failed", "message": "Vendor ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        services =Service.objects.filter(vendor_id=vendor_id)  # ✅ Corrected filtering

        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.renderers import JSONRenderer   
class ViewsshopView(viewsets.ReadOnlyModelViewSet):
    queryset = Vendor_addShop.objects.all()
    serializer_class = VendoraddShopSerializer
    renderer_classes = [JSONRenderer]  

    def list(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor_id')

        # ✅ Ensure vendor_id is passed
        if not vendor_id:
            return Response({"status": "failed", "message": "Vendor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor_id = int(vendor_id)
        except ValueError:
            return Response({"status": "failed", "message": "Invalid Vendor ID."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Fetch shops based on vendor_id
        shops = Vendor_addShop.objects.filter(vendor_id=vendor_id)  
        if not shops.exists():
            return Response({"status": "failed", "message": "No shops found for this vendor."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(shops, many=True, context={"request": request})  
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
from django.shortcuts import get_object_or_404
from jsonschema import ValidationError
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from userapp.models import User
from userapp.serializers import UserSerializer
from .models import Vendor
from .serializers import VendorSerializer
from .serializers import *

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    http_method_names=['post']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
             instance = serializer.save()
             return Response(
                {
                    "status": "success",
                    "message": "Vendor created successfully!",
                    "vendor_id": instance.id
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "status": "error",
                "message": "Invalid data provided.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST  
        )

from rest_framework import generics
from .models import Service
from .serializers import ServiceSerializer
from vendor.serializers import VendorSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    http_method_names = ['post']
    serializer_class = ServiceSerializer

    def post(self, request, *args, **kwargs):
        """Custom POST response for creating a new service"""
        vendor_id = request.data.get("vendor_id")  

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save() 

            return Response(
                {
                    "message": "Service created successfully",
                    "status": "success",
                    "service_id": service.id,  
                    "vendor_id": vendor_id, 
                },
                status=status.HTTP_201_CREATED,  
            )

        return Response(
            {
                "message": "Failed to create service",
                "status": "error",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


from rest_framework.response import Response
from rest_framework import status

def get(self, request, *args, **kwargs):
    """Custom GET response for retrieving services"""
    services = self.get_queryset()
    serializer = self.get_serializer(services, many=True)
    
    # Return the list directly instead of wrapping it inside "data"
    return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer
class VendorLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor = Vendor.objects.get(email=email)

            # Validate password securely
            if password==vendor.password:
                serializer = VendorSerializer(vendor)
                return Response({"message": "Login successful","vendor_id": vendor.id, "Role":"Vendor","status": vendor.status}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


class VendoraddShopListCreateView(generics.ListCreateAPIView):
    queryset = Vendor_addShop.objects.all()
    serializer_class = VendoraddShopSerializer
    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images'    )  # ✅ Multiple images
        shop_image = request.FILES.get('shop_image')  # ✅ Main shop image

        # ✅ Pass shop_image during save
        serializer = self.get_serializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            shop = serializer.save(shop_image=shop_image)  # ✅ Save main image

            # ✅ Save additional work images
            for image in images:
                Vendor_ShopImage.objects.create(shop=shop, image=image)

            return Response(
                {
                    "message": "Vendor Shop added successfully!",
                    "status": "success",
                    "vendor_id": shop.vendor.id,
                    "data": VendoraddShopSerializer(shop, context={"request": request}).data,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VendoraddShopRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor_addShop.objects.all()
    serializer_class = VendoraddShopSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Vendor Shop deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
class VendorServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    http_method_names = ['get', 'delete']  # Allow DELETE requests

    def list(self, request, *args, **kwargs):
        vendor_id = request.query_params.get("vendor_id")

        if not vendor_id:
            return Response({"error": "Valid vendor_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        vendor = get_object_or_404(Vendor, id=int(vendor_id))
        services = Service.objects.filter(vendor_id=vendor_id)
        services_data = self.get_serializer(services, many=True).data  

        # Format the response with vendor ID only
        formatted_services = [
            {
                "id": service["id"],
                "service_name": service["service_name"],
                "details": service["details"],
                "total_amount": service["total_amount"],
                "vendor": vendor.id
            }
            for service in services_data
        ]

        return Response(formatted_services, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        service_id = request.query_params.get("service_id")

        if not service_id:
            return Response({"error": "service_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = get_object_or_404(Service, id=int(service_id))

        service.delete()  # Delete the service

        return Response({"message": "Service deleted successfully"}, status=status.HTTP_200_OK)
    
class VendorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorSerializer  
    http_method_names = ['get', 'patch', 'post']

    def get_object(self):
        vendor_id = self.request.query_params.get("vendor_id")
        if not vendor_id:
            raise ValidationError({"error": "vendor_id is required"})
        return get_object_or_404(Vendor, id=vendor_id)

    def get(self, request, *args, **kwargs):
        """Retrieve vendor details along with their services."""
        vendor = self.get_object()
        services = Service.objects.filter(vendor_id=vendor.id)
        services_data = ServiceSerializer(services, many=True).data 

        return Response({
            "vendor_id": vendor.id,
            "name": vendor.name,
            "email": vendor.email,
            "mobile_no": vendor.mobile_no,
            "category": vendor.category,
            "status": vendor.status,
            "services": services_data
        }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """Update vendor details partially."""
        vendor = self.get_object()
        serializer = VendorSerializer(vendor, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vendor updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ViewservicesView(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        vendor_id = request.query_params.get('vendor_id')  # Corrected query param name
        print(request.query_params)
        if not vendor_id:
            return Response(
                {"status": "failed", "message": "Vendor ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        services =Service.objects.filter(vendor_id=vendor_id)  # Corrected filtering

        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class ViewsshopView(viewsets.ModelViewSet):  
    """Handles retrieving shop details."""
    
    queryset = Vendor_addShop.objects.all()
    serializer_class = VendoraddShopSerializer
    renderer_classes = [JSONRenderer]
    parser_classes = (MultiPartParser, FormParser)  

    def list(self, request, *args, **kwargs):
        """Retrieve shop details based on vendor_id."""
        vendor_id = request.query_params.get('vendor_id')

        if not vendor_id:
            return Response({"status": "failed", "message": "Vendor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor_id = int(vendor_id)
        except ValueError:
            return Response({"status": "failed", "message": "Invalid Vendor ID."}, status=status.HTTP_400_BAD_REQUEST)

        vendor_shops = Vendor_addShop.objects.filter(vendor_id=vendor_id)
        serializer = self.get_serializer(vendor_shops, many=True)

        if serializer.data:
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_200_OK)
        
# class VendorShopUpdateView(APIView):
#     parser_classes = [MultiPartParser, FormParser]  # ✅ Ensure correct parsers for file upload

#     def put(self, request, *args, **kwargs):
#         return self.update_images(request, replace=True)

#     def update_images(self, request, replace):
#         vendor_id = request.data.get("vendor_id")

#         if not vendor_id:
#             return Response({"error": "vendor_id is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             vendor_id = int(vendor_id)
#         except ValueError:
#             return Response({"error": "Invalid vendor_id"}, status=status.HTTP_400_BAD_REQUEST)

#         shop = get_object_or_404(Vendor_addShop, vendor_id=vendor_id)

#         # ✅ Extracting multiple images from request.FILES
#         images = request.FILES.getlist("work_images")  # Ensure frontend sends images as "work_images[]"

#         print(f"Request Received: vendor_id={vendor_id}, replace={replace}, files={images}")

#         if not images:
#             return Response({"error": "At least one image is required"}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = VendorWorkImageUpdateSerializer(data={"work_images": images})

#         if serializer.is_valid():
#             serializer.update(shop, serializer.validated_data, replace=replace)
#             return Response({"status": "success", "message": "Work images updated successfully"}, status=status.HTTP_200_OK)

#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class VendorShopImageUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        shop_id = request.data.get('shop')  # Get shop ID from request
        images = request.FILES.getlist('work_images')  # Get multiple images

        if not shop_id:
            return Response({'error': 'Shop ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shop = Vendor_addShop.objects.get(id=shop_id)  # Fetch shop instance
        except Vendor_addShop.DoesNotExist:
            return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorWorkImageUpdateSerializer(data={'work_images': images})
        if serializer.is_valid():
            serializer.update(shop, serializer.validated_data, replace=True)
            return Response({'status':'success',
                             'message': 'Images updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class VendorViewbookings(viewsets.ModelViewSet):
    queryset = servicebooking.objects.all()
    serializer_class = VendorbookingSerializer    
    http_method_names = ["get"]  # Allow only GET and POST

    def list(self, request, *args, **kwargs):
        """List all vendors or filter by ID."""
        vendor_id = request.query_params.get("id")
        
        if vendor_id:
            try:
                vendor = servicebooking.objects.get(id=vendor_id)
                serializer = self.get_serializer(vendor)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response({"error": "Vendor not found."}, status=404)
        
        # If no ID is provided, return all vendors
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """Create a new vendor."""
        return super().create(request, *args, **kwargs)
    
    
class GooglePayPaymentView(generics.ListCreateAPIView):
    serializer_class = GooglePayPaymentSerializer
    http_method_names = ["get"] 
    def get_queryset(self):
        return Payment.objects.filter(payment_method="googlepay")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({
                "message": "Google Pay payment successful!",
                "status": "success",
                "payment_id": payment.id,
                "data": serializer.data
            }, status=status.HTTP_200_OK)  # ✅ Changed from 201 to 200
        return Response({
            "message": "Payment failed due to invalid data.",
            "status": "failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)  # ✅ Kept 400 for errors


# ✅ Card Payment View (POST & GET)
class CardPaymentView(generics.ListCreateAPIView):
    serializer_class = CardPaymentSerializer
    http_method_names = ["get"] 
    def get_queryset(self):
        return Payment.objects.filter(payment_method="card")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({
                "message": "Card payment successful!",
                "status": "success",
                "payment_id": payment.id,
                "data": serializer.data
            }, status=status.HTTP_200_OK)  # ✅ Changed from 201 to 200
        return Response({
            "message": "Payment failed due to invalid data.",
            "status": "failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)  # ✅ Kept 400 for errors

class VendorFeedbackListCreateView(generics.ListCreateAPIView):
    queryset = UserFeedback.objects.all()
    serializer_class = VendorFeedbackSerializer
    http_method_names = ['get']  # Allow only GET and POST


class VendorServiceBookingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        vendor_id = request.query_params.get("vendor_id")

        # ✅ Validate vendor_id
        if not vendor_id:
            return Response(
                {"error": "Vendor ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Fetch bookings for the given vendor
        bookings = servicebooking.objects.filter(vendor_id=vendor_id).select_related('service', 'user')

        if not bookings.exists():
            return Response(
                {"message": "No bookings found for this vendor."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Serialize and return the bookings
        serializer = VendorServiceBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ConfirmServiceBookingAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")

        # ✅ Validate booking_id
        if not booking_id:
            return Response(
                {"error": "Booking ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ✅ Fetch the booking instance
            booking = servicebooking.objects.get(id=booking_id)
        except servicebooking.DoesNotExist:
            return Response(
                {"error": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Check if the booking is currently 'booked'
        if booking.status == "booked":
            booking.status = "confirm"  # ✅ Update status to 'confirm'
            booking.save()

            return Response(
                {"message": "Booking status updated to 'confirm' successfully.",
                 "status": "success"},
                status=status.HTTP_200_OK         
            )
        else:
            return Response(
                {"error": f"Booking status is currently '{booking.status}'. Only 'booked' status can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
class RejectServiceBookingAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        booking_id = request.data.get("booking_id")

        # ✅ Validate booking_id
        if not booking_id:
            return Response(
                {"error": "Booking ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # ✅ Fetch the booking instance
            booking = servicebooking.objects.get(id=booking_id)
        except servicebooking.DoesNotExist:
            return Response(
                {"error": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Check if the booking is currently 'booked'
        if booking.status == "booked":
            booking.status = "rejected"  # ✅ Update status to 'rejected'
            booking.save()

            return Response(
                {"message": "Booking status updated to 'rejected' successfully.",
                 "status": "success"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": f"Booking status is currently '{booking.status}'. Only 'booked' status can be rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
class VendorFeedbackListCreateView(generics.ListCreateAPIView):
    queryset = UserFeedback.objects.all()
    serializer_class = VendorFeedbackSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Override create to return custom success response"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()  # Save feedback
            response_data = {
                "status": "success",
                **VendorFeedbackSerializer(feedback).data  # ✅ Merging serialized data directly
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )  
        