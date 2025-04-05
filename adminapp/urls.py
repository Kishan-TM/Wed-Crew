from django.urls import path
from .views import *

from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),  # Login page
    path('index/', views.index, name='index'), 
     path('basic/', views.basic, name='basic'),# Admin Dashboard (Index page)
    path('logout/', views.admin_logout, name='admin_logout'), 
     path('add_package/',views.add_package, name='add_package'),
    path("edit_event_package/", views.edit_event_package, name="edit_event_package"),
      path('premium/', views.premium, name='premium'),
        path('luxury/', views.luxury, name='luxury'),
    path('edit/<int:package_id>/',views.edit_package, name='edit_package'),
     path('delete/<int:package_id>/',views.delete_package, name='delete_package'),
      path('basic_packageslist/', views.basic_packageslist, name='basic_packageslist'),
      path('luxury_packageslist/', views.luxury_packageslist, name='luxury_packageslist'),
      path('premium_packageslist/', views.premium_packageslist, name='premium_packageslist'),
      path('users_list/', views.users_list, name='users_list'),
      path('vendor_list/', views.vendor_list, name='vendor_list'),
      path('booking_list/',views.booking_list, name='booking_list'),
      path('packages/', views.packages_list, name='packages_list'),
      path('logout/', views.logout, name='logout'), 
       path('vendor/approve/<int:vendor_id>/', approve_vendor, name='approve_vendor'),
    path('vendor/reject/<int:vendor_id>/', reject_vendor, name='reject_vendor'),
       path('bookings/approve/<int:booking_id>/',views.approve_booking, name='approve_booking'),
    path('bookings/reject/<int:booking_id>/',views.reject_booking, name='reject_booking'),
    path('payments/',views.payment_list, name='payment_list'),
    path("user_feedback/", views.view_user_feedback, name="user_feedback"),
    path("vendor_feedbacks/", views.view_vendor_feedback, name="vendor_feedbacks"),
    
]

