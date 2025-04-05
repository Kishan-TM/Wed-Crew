from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import EventPackageListCreateView, UserListCreateView, UserRetrieveUpdateDestroyView
from .views import *
# Router

schema_view = get_schema_view(
    openapi.Info(
        title="Event API",
        default_version="v1",
        description="API documentation for the event app.",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"servicebookings",ServiceBookingView,basename='servicebooking')

urlpatterns = [
   re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path("packages/", EventPackageListCreateView.as_view(), name="list_create_packages"),
    path('userviewservices/', ServiceListView.as_view(), name='user-view-services'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('services/', UserViewServices.as_view({'get': 'list'}), name='services'),
    path('event-packages/',EventPackagesListView.as_view(), name='event-packages'),
    path("googlepay_payment/", GooglePayPaymentView.as_view(), name="googlepay-payment"),
    path("card_payment/", CardPaymentView.as_view(), name="card_payment"),
    path("eventpayment/googlepay/", eventGooglePayPaymentView.as_view(), name="googlepay-payment"),
    path("eventpayment/card/", eventCardPaymentView.as_view(), name="card-payment"),
    path("servicescategory/", ServiceCategoryViewSet.as_view({"get": "list"}), name="service-list"),
    path('photography/', PhotographyServiceListView.as_view(), name='photography-services'),
    path('venue-coordinator/', VenueCoordinatorServiceListView.as_view(), name='venue-coordinator-services'),
    path('decor-coordinator/', DecorCoordinatorServiceListView.as_view(), name='decor-coordinator-services'),
    path('beautician/', BeauticianServiceListView.as_view(), name='beautician-services'),
    path('servicesdetails/',  VendorServicedetailView.as_view({'get': 'list'}), name='service-list'),
    path('user-feedbacks/', UserFeedbackListCreateView.as_view(), name='feedback-list'),
    path("user_service_bookings/", UserServiceBookingAPIView.as_view(), name="user_service_bookings"),
    path("user_package_bookings/", UserPackageBookingAPIView.as_view(), name="user_package_bookings"),
    # path("submit-feedback/", SubmitFeedbackView.as_view(), name="submit-feedback"),
    path('', include(router.urls)),
    
]
