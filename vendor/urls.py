from django.urls import path
from .views import *
from django.urls import path, re_path
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import (
    VendorListCreateView, 
    
    ServiceListCreateView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Vendor API",
        default_version="v1",
        description="API documentation for Vendor Management",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    # Vendor Endpoints
    path("vendors/", VendorListCreateView.as_view(), name="vendor-list-create"),
    path("servicesbookings/", VendorViewbookings.as_view({"get": "list"}), name="vendor-list"),
    path('login/', VendorLoginView.as_view(), name='vendor-login'),
    path("services/", ServiceListCreateView.as_view(), name="service-list-create"),
    path('view-services/', ViewservicesView.as_view({'get': 'list'}), name='view-services'),
    path("vendor-services/", VendorServiceListView.as_view(), name="vendor-service-list"),
    path('vendor-shops/', VendoraddShopListCreateView.as_view(), name='vendor-shop-list-create'),
    path('profile/', VendorProfileView.as_view(), name='vendor-profile'),
    path('view-shop/', ViewsshopView.as_view({'get': 'list'}), name='view-shop'),
    path('update-shop/', VendorShopImageUpdateView.as_view(), name='update-shop'), 
    path("payments/googlepay/", GooglePayPaymentView.as_view(), name="googlepay_payment"),
    path("payments/card/", CardPaymentView.as_view(), name="card_payment"),
    path('vendor-feedback/',VendorFeedbackListCreateView.as_view(), name='vendor-feedback'),
    path("vendor_service_bookings/", VendorServiceBookingAPIView.as_view(), name="vendor-service-bookings"),
    path("booking/confirm/", ConfirmServiceBookingAPIView.as_view(), name="confirm-booking"),
    path("booking/reject/", RejectServiceBookingAPIView.as_view(), name="reject-booking"),
    
    
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
