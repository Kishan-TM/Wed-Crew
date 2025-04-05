

# Create your views here.
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserFeedbackSerializer, VendorServiceExtendedSerializer, ViewServiceBookingSerializer 
from adminapp.models import EventPackage
from vendor.models import Payment, Service, servicebooking, UserFeedback, Vendor, Vendor_addShop
from vendor.serializers import ServiceSerializer, VendorSerializer, VendoraddShopSerializer
from .serializers import CardPaymentSerializer, EventPackageSerializer, EventPackagesSerializer, GooglePayPaymentSerializer, ServiceBookingSerializer, UserSerializer, eventCardPaymentSerializer, eventGooglePayPaymentSerializer, usercategorySerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework import generics,viewsets
from .models import *
from .serializers import BookingSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from userapp.models import User
from userapp.serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from userapp.models import User
from userapp.serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from userapp.models import User
from userapp.serializers import UserSerializer
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Registration successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRetrieveUpdateDestroyView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class EventPackagesListView(generics.ListAPIView):
    queryset = EventPackage.objects.all()
    serializer_class = EventPackagesSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        print(serializer.data)  # Debugging

        data_list = [
            {
                "id":item['id'],
                "name": item["name"],
                "image": item["image"],
            }
            for item in serializer.data
        ]

        return Response(data_list, status=status.HTTP_200_OK)



class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Booking created successfully!",
                "id": serializer.instance.id,  # Correct way to get the booking ID
                "data": serializer.data
            },
            status=status.HTTP_200_OK  # Success response with status 200
        )

class EventPackageListCreateView(generics.ListCreateAPIView):
    serializer_class = EventPackageSerializer
    http_method_names = ['get']

    def get_queryset(self):
        """Filter event packages based on the provided 'id' in query parameters."""
        id = self.request.query_params.get('id')  # Get 'id' from request query parameters
        if id:
            return EventPackage.objects.filter(id=id)  # Filter by ID if provided
        return EventPackage.objects.none()  # Return an empty queryset if no ID is provided

    def list(self, request, *args, **kwargs):
        """Handle GET requests to return the requested event package."""
        id = request.query_params.get('id')

        if not id:
            return Response({"status": "failed", "message": "Event Package ID is required."}, status=400)

        try:
            package = EventPackage.objects.get(id=id)
            serializer = self.get_serializer(package)
            return Response(serializer.data)
        except EventPackage.DoesNotExist:
            return Response({"status": "failed", "message": "Event package not found."}, status=404)

class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user=User.objects.get(email=email,password=password)

        if user:
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "role":"user"
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer  # ✅ Uses UserSerializer for consistency

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)  # ✅ Get the user or return 404

        return Response({
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        }, status=status.HTTP_200_OK)
        
        
        
class UserViewServices(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def list(self, request, *args, **kwargs):
        service_name = request.query_params.get('service')  # ✅ Renamed to service_name for clarity
        
        if service_name:
            queryset = Service.objects.filter(service_name__icontains=service_name)  # ✅ Case-insensitive filtering
        else:
            queryset = Service.objects.all()  # ✅ Return all services if no filter is provided

        if not queryset.exists():
            return Response(
                {"status": "failed", "message": "No services found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)

from rest_framework import viewsets, status
from rest_framework.response import Response
from vendor.models import servicebooking
from vendor.models import Service
from .serializers import ServiceBookingSerializer

class ServiceBookingView(viewsets.ModelViewSet):
    queryset = servicebooking.objects.all()
    serializer_class = ServiceBookingSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        user = request.data.get("user")  # Optional, can be NULL
        service_ids = request.data.get("service_ids")  # Expecting a list of service IDs
        advanced_price = request.data.get("advanced_price")
        time = request.data.get("time")
        date = request.data.get("date", None)  # Get date or leave it as None
        address = request.data.get("address")
        vendor_id = request.data.get("vendor")

        # ✅ Validate required fields
        if not service_ids or not advanced_price or not time or not address or not vendor_id:
            return Response({"error": "All fields are required, including vendor."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Validate service_ids as a list
        if not isinstance(service_ids, list):
            return Response({"error": "Service IDs should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Fetch the vendor instance
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Check if all services exist
        services = Service.objects.filter(id__in=service_ids)
        if not services.exists():
            return Response({"error": "One or more services do not exist."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Create multiple bookings
        bookings = []
        for service in services:
            booking = servicebooking.objects.create(
                user_id=user,  # Can be NULL if not provided
                service=service,
                advanced_price=advanced_price,
                time=time,
                date=date,  # May be NULL if not provided
                address=address,
                vendor=vendor  # ✅ Pass the vendor instance here
            )
            bookings.append(booking)

        # ✅ Serialize all created bookings
        serializer = ServiceBookingSerializer(bookings, many=True)
        return Response(
            {"status": "success", "message": "Service(s) booked successfully.", "bookings": serializer.data},
            status=status.HTTP_201_CREATED
        )


class UserServiceBookingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get("user_id")

        # ✅ Validate user_id
        if not user_id:
            return Response(
                {"error": "User ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Fetch bookings for the given user
        bookings = servicebooking.objects.filter(user_id=user_id).select_related('service', 'vendor')

        if not bookings.exists():
            return Response(
                {"message": "No bookings found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # ✅ Serialize and return the bookings
        serializer = ViewServiceBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):  # Only allows GET
    queryset = Service.objects.all()
    serializer_class = usercategorySerializer
    http_method_names = ["get"]  # Restrict to GET requests

    def list(self, request, *args, **kwargs):
        """Filter services by service name if provided."""
    
        service_name = request.query_params.get("service_name", None)

        # services = self.get_queryset()  # Ensures proper queryset evaluation

        # Case-insensitive service name filtering
        if service_name:
            services = Service.objects.filter(service_name=service_name)  # Partial match on service name

        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
# class GooglePayPaymentView(generics.CreateAPIView):
#     serializer_class = GooglePayPaymentSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             payment = serializer.save()
#             return Response({
#                 "message": "Google Pay payment successful!",
#                 "status": "success",
#                 "payment_id": payment.id
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GooglePayPaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = GooglePayPaymentSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user")
        booking_ids = request.data.get("booking_ids")  # List of booking IDs
        amount_paid = request.data.get("amount_paid")
        upi_id = request.data.get("upi_id")  # UPI ID for Google Pay

        # ✅ Validate required fields
        if not user_id or not booking_ids or not amount_paid or not upi_id:
            return Response(
                {"error": "All fields (user, booking_ids, upi_id, and amount_paid) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Validate if booking_ids is a list
        if not isinstance(booking_ids, list):
            return Response({"error": "Booking IDs should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Fetch valid bookings
        bookings = servicebooking.objects.filter(id__in=booking_ids, status="pending")
        if not bookings.exists():
            return Response({"error": "One or more bookings do not exist or are already paid."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Create payment for each booking
        payments = []
        for booking in bookings:
            # ✅ Validate amount paid matches the booking price
            if Decimal(str(amount_paid)) != booking.advanced_price:
                return Response(
                    {"error": f"Amount paid for booking {booking.id} does not match the required price."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment_data = {
                "booking": booking.id,
                "user": user_id,
                "payment_method": "googlepay",
                "amount_paid": amount_paid,
                "upi_id": upi_id,
            }

            # ✅ Serialize and save Google Pay payment
            serializer = self.get_serializer(data=payment_data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    payments.append(serializer.data)

                    # ✅ Update booking status to "booked" after successful payment
                    booking.status = "booked"
                    booking.save()
                except Exception as e:
                    return Response(
                        {"error": f"An error occurred while processing payment: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Return success response with payment details
        return Response(
            {"status": "success", "message": "Google Pay payment(s) processed successfully.", "payments": payments},
            status=status.HTTP_201_CREATED,
        )


# ✅ Card Payment View
# class CardPaymentView(generics.CreateAPIView):
#     serializer_class = CardPaymentSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             payment = serializer.save()
#             return Response({
#                 "message": "Card payment successful!",
#                 "status": "success",
#                 "payment_id": payment.id
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CardPaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CardPaymentSerializer

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("user")
        booking_ids = request.data.get("booking_ids")  # List of booking IDs
        amount_paid = request.data.get("amount_paid")
        card_number = request.data.get("card_number")
        cardholder_name = request.data.get("cardholder_name")
        expiry_date = request.data.get("expiry_date")
        cvv_number = request.data.get("cvv_number")

        # ✅ Validate required fields
        if not user_id or not booking_ids or not amount_paid:
            return Response(
                {"error": "All fields (user, booking_ids, card details, and amount_paid) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Validate if booking_ids is a list
        if not isinstance(booking_ids, list):
            return Response({"error": "Booking IDs should be a list."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Fetch valid bookings
        bookings = servicebooking.objects.filter(id__in=booking_ids, status="pending")
        if not bookings.exists():
            return Response({"error": "One or more bookings do not exist or are already paid."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Create payment for each booking
        payments = []
        for booking in bookings:
            # ✅ Validate amount paid matches the booking price
            if Decimal(str(amount_paid)) != booking.advanced_price:
                return Response(
                    {"error": f"Amount paid for booking {booking.id} does not match the required price."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment_data = {
                "booking": booking.id,
                "user": user_id,
                "payment_method": "card",
                "amount_paid": amount_paid,
                "card_number": card_number,
                "cardholder_name": cardholder_name,
                "expiry_date": expiry_date,
                "cvv_number": cvv_number,
            }

            # ✅ Serialize and save card payment
            serializer = self.get_serializer(data=payment_data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    payments.append(serializer.data)

                    # ✅ Update booking status to "booked" after successful payment
                    booking.status = "booked"
                    booking.save()
                except Exception as e:
                    return Response(
                        {"error": f"An error occurred while processing payment: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Return success response with payment details
        return Response(
            {"status": "success", "message": "Card Payment(s) processed successfully.", "payments": payments},
            status=status.HTTP_201_CREATED,
        )
    
    
class eventGooglePayPaymentView(generics.CreateAPIView):
    serializer_class = eventGooglePayPaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({
                "message": "Google Pay payment successful!",
                "status": "success",
                "payment_id": payment.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Card Payment View
class eventCardPaymentView(generics.CreateAPIView):
    serializer_class = eventCardPaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({
                "message": "Card payment successful!",
                "status": "success",
                "payment_id": payment.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PhotographyServiceListView(generics.ListAPIView):
    serializer_class = VendoraddShopSerializer

    def get_queryset(self):
        return Vendor_addShop.objects.filter(vendor__category="Photography")  # Correct field reference

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No photography services found."}, status=status.HTTP_404_NOT_FOUND)  # Fixed status code
        
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)

class VenueCoordinatorServiceListView(generics.ListAPIView):
    serializer_class = VendoraddShopSerializer

    def get_queryset(self):
        return Vendor_addShop.objects.filter(vendor__category="Venue Coordinator")  # Correct field reference

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No venue coordinator services found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class DecorCoordinatorServiceListView(generics.ListAPIView):
    serializer_class = VendoraddShopSerializer

    def get_queryset(self):
        return Vendor_addShop.objects.filter(vendor__category="Decor Coordinator")  # Correct field reference

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No decor coordinator services found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class BeauticianServiceListView(generics.ListAPIView):
    serializer_class = VendoraddShopSerializer

    def get_queryset(self):
        return Vendor_addShop.objects.filter(vendor__category="Beautician")  # Correct field reference

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No beautician services found."}, status=status.HTTP_404_NOT_FOUND)
        
        data = self.get_serializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
class VendorServicedetailView(viewsets.ModelViewSet):
    """Handles retrieving vendor services."""
    
    queryset = Service.objects.all()
    serializer_class = VendorServiceExtendedSerializer
    renderer_classes = [JSONRenderer]
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        """Retrieve services based on vendor_id."""
        vendor_id = request.query_params.get('vendor_id')

        if not vendor_id:
            return Response({"status": "failed", "message": "Vendor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vendor_id = int(vendor_id)
        except ValueError:
            return Response({"status": "failed", "message": "Invalid Vendor ID."}, status=status.HTTP_400_BAD_REQUEST)

        services = Service.objects.filter(vendor__id=vendor_id)  # ✅ Fixed vendor_id reference
        serializer = self.get_serializer(services, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class UserFeedbackListCreateView(generics.ListCreateAPIView):
#     queryset = UserFeedback.objects.all()
#     serializer_class = UserFeedbackSerializer
#     http_method_names = ['post']
#     def perform_create(self, serializer):
#         serializer.save()  # No user assignment, as authentication is removed
      
class UserFeedbackListCreateView(generics.ListCreateAPIView):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """Override create to return custom success response"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save()  # Save feedback
            response_data = {
                "status": "success",
                **UserFeedbackSerializer(feedback).data  # ✅ Merging serialized data directly
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


    
    
