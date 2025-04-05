from importlib.resources import Package
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from userapp.models import Booking, User
from vendor.models import Payment, Vendor
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
# Admin login view
from django.shortcuts import render, redirect
from django.contrib import messages

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Hardcoded credentials for admin login (for testing purposes)
        if email == 'admin@gmail.com' and password == '12345':
            # Set session variables
            request.session['admin_logged_in'] = True
            request.session['admin_email'] = email
            return redirect('index')  # Redirect to index/dashboard after login
        else:
            messages.error(request, "Invalid Email or Password")

    return render(request, 'login.html')

# Admin dashboard view
def index(request):
    if not request.session.get('admin_logged_in'):
        return redirect('login')  # Redirect to login if not logged in
    return render(request, 'index.html')

# Admin logout view
def admin_logout(request):
    # Clear the session data
    request.session.flush()
    return redirect('admin_login')  # Redirect to login after logout

from django.shortcuts import render

def basic(request):
    packages = EventPackage.objects.filter(name="Basic")  # Fetch all packages
    return render(request, 'basic.html', {'packages': packages})


from django.shortcuts import render, redirect
from .models import EventPackage
def add_package(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        max_guests = request.POST.get("max_guests")
        services = request.POST.get("services")
        extra_services = request.POST.get("extra_services", "")

        # Debug: Print the values to check if they are being retrieved correctly
        print(f"Name: {name}, Price: {price}, Max Guests: {max_guests}, Services: {services}, Extra Services: {extra_services}")

        # Create and save the package
        EventPackage.objects.create(
            name=name,
            price=price,
            max_guests=max_guests,
            services=services,
            extra_services=extra_services
        )

        return redirect("add_package")  # Redirect to the same view to refresh the page

    # Fetch existing packages to display
    packages = EventPackage.objects.all()
    return render(request, "add_package.html", {"packages": packages})

def list_packages(request):
    packages = EventPackage.objects.all()
    return render(request, 'list_packages.html', {'packages': packages})

from django.shortcuts import render, get_object_or_404, redirect
from .models import EventPackage

def edit_event_package(request):
    package_id = request.GET.get('id')
    package = get_object_or_404(EventPackage, id=package_id)

    if request.method == "POST":
        package.name = request.POST.get("name")
        package.price = float(request.POST.get("price", package.price))  # Convert to float
        package.max_guests = int(request.POST.get("max_guests", package.max_guests))  # Convert to int
        package.services = request.POST.get("services")
        package.extra_services = request.POST.get("extra_services")

        package.save()

        return redirect("packages_list")  # Redirect to an actual working view

    return render(request, "edit_event_package.html", {"package": package})

def delete_package(request, package_id):
    package = get_object_or_404(EventPackage, id=package_id)  # Ensure correct model
    package.delete()
    messages.success(request, "Package deleted successfully!")
    return redirect('packages_list')  # Ensure this matches your URL name Redirect back to package li

def premium(request):
    packages = EventPackage.objects.filter(name="Premium")  # Fetch all packages
    return render(request, 'premium.html', {'packages': packages})

def luxury(request):
    packages = EventPackage.objects.filter(name="Luxury")  # Fetch all packages
    return render(request, 'luxury.html', {'packages': packages})

def basic_packageslist(request):
    """View to list only Basic event packages."""
    basic_packages = EventPackage.objects.filter(name="Basic")  # Adjust field name if needed
    return render(request, "basic_packageslist.html", {"packages": basic_packages})

def luxury_packageslist(request):
    """View to list only Luxury event packages."""
    luxury_packages = EventPackage.objects.filter(name="Luxury")  # Adjust field name if needed
    return render(request, "luxury_packageslist.html", {"packages": luxury_packages})

def premium_packageslist(request):
    """View to list only Premium event packages."""
    premium_packages = EventPackage.objects.filter(name="Premium")  # Adjust field name if needed
    return render(request, "premium_packageslist.html", {"packages": premium_packages})

def users_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendor_list.html', {'vendors': vendors})

def booking_list(request):
    bookings = Booking.objects.all().order_by('-date_of_marriage')  # Show latest first
    return render(request, 'booking_list.html', {'bookings': bookings})

def packages_list(request):
    packages = EventPackage.objects.all()
    return render(request, 'packages_list.html', {'packages': packages})

def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return render(request,'index.html')

def edit_package(request, package_id):
    package = get_object_or_404(EventPackage, id=package_id)

    if request.method == 'POST':
        package.name = request.POST.get('name')
        package.price = request.POST.get('price')
        package.max_guests = request.POST.get('max_guests')
        package.services = request.POST.get('services')
        package.extra_services = request.POST.get('extra_services')
        package.save()
        return redirect('packages_list')  # Change to your package listing page name

    return render(request, 'edit_event_package.html', {'package': package})

def approve_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    # ✅ Allow re-approval of rejected vendors
    if vendor.status in ['pending', 'rejected']:
        vendor.status = 'approved'
        vendor.save()
        messages.success(request, f"Vendor {vendor.name} has been approved.")
    else:
        messages.info(request, f"Vendor {vendor.name} is already approved.")

    return redirect('vendor_list')  # Ensure 'vendor_list' is your actual URL name

def reject_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    # ✅ Allow rejecting even after approval (if needed)
    if vendor.status != 'rejected':
        vendor.status = 'rejected'
        vendor.save()
        messages.error(request, f"Vendor {vendor.name} has been rejected.")
    
    return redirect('vendor_list')  # Ensure 'vendor_list' is your actual URL name
def approve_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = "confirmed"
    booking.save()
    messages.success(request, "Booking confirmed successfully.")
    return redirect("booking_list")

def reject_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = "cancelled"
    booking.save()
    messages.error(request, "Booking has been cancelled.")
    return redirect("booking_list")

def payment_list(request):
    payments = EventPayment.objects.all()
    return render(request, 'payment_list.html', {'payments': payments})

from userapp.models import UserFeedback

def view_user_feedback(request):
    feedbacks = UserFeedback.objects.all().order_by("-created_at")
    return render(request, "user_feedback.html", {"feedbacks": feedbacks})

from vendor.models import VendorFeedback

def view_vendor_feedback(request):
    feedbacks = VendorFeedback.objects.all().order_by("-created_at")
    return render(request, "vendor_feedback.html", {"feedbacks": feedbacks})

