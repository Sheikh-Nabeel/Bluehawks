from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import ContactSubmission, AirportBooking, Service


def home(request):
    context = {
        'meta_title': 'Bluehawks Security Services - Professional Security Solutions in Pakistan',
        'meta_description': 'Bluehawks Security Services provides comprehensive security solutions including airport transportation, security training, and professional security services across Pakistan.',
        'meta_keywords': 'security services, airport transportation, security training, Pakistan, Bluehawks, professional security',
    }
    return render(request, 'mainwebsite/home.html', context)

def about(request):
    context = {
        'meta_title': 'About Bluehawks Security Services - Your Trusted Security Partner',
        'meta_description': 'Learn about Bluehawks Security Services, our mission, values, and commitment to providing professional security solutions in Pakistan.',
        'meta_keywords': 'about Bluehawks, security company Pakistan, professional security services',
    }
    return render(request, 'mainwebsite/about.html', context)

def services(request):
    services_list = Service.objects.filter(is_active=True)
    context = {
        'meta_title': 'Security Services - Bluehawks Professional Security Solutions',
        'meta_description': 'Explore our comprehensive range of security services including airport transportation, security training, and professional security solutions.',
        'meta_keywords': 'security services, airport transportation, security training, professional security',
        'services': services_list,
    }
    return render(request, 'mainwebsite/services.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        city = request.POST.get("city", "")
        message = request.POST.get("message", "")
        if name and email and message:
            ContactSubmission.objects.create(
                name=name,
                email=email,
                phone=phone,
                city=city,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect("/contact/")
        else:
            messages.error(request, "Please fill in all required fields.")
    
    context = {
        'meta_title': 'Contact Bluehawks Security Services - Get in Touch',
        'meta_description': 'Contact Bluehawks Security Services for professional security solutions, airport transportation, and security training. Located in Islamabad, Pakistan.',
        'meta_keywords': 'contact Bluehawks, security services contact, Islamabad security company',
    }
    return render(request, 'mainwebsite/contact.html', context)

def clients(request):
    context = {
        'meta_title': 'Our Clients - Bluehawks Security Services',
        'meta_description': 'Discover the trusted clients and organizations that rely on Bluehawks Security Services for their security needs.',
        'meta_keywords': 'Bluehawks clients, security services clients, trusted security company',
    }
    return render(request, 'mainwebsite/clients.html', context)

def airport_bookings(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        pickup_airport = request.POST.get("pickup_airport", "")
        destination = request.POST.get("destination", "")
        travel_date = request.POST.get("travel_date", "")
        passengers = request.POST.get("passengers", "")
        message = request.POST.get("message", "")
        if name and email and phone and pickup_airport and destination and travel_date:
            AirportBooking.objects.create(
                name=name,
                email=email,
                phone=phone,
                passengers=passengers,
                pickup_airport=pickup_airport,
                destination=destination,
                travel_date=travel_date,
                message=message
            )
            messages.success(request, "Your airport booking request has been sent successfully!")
            return redirect("/airport-bookings/")
        else:
            messages.error(request, "Please fill in all required fields.")
    
    context = {
        'meta_title': 'Airport Bookings & Transportation - Bluehawks Security Services',
        'meta_description': 'Professional airport pickup and drop-off services across Pakistan. Reliable transportation to and from major airports with security-trained drivers.',
        'meta_keywords': 'airport transportation, airport pickup, airport drop-off, Pakistan airports, security transportation',
    }
    return render(request, 'mainwebsite/airport_bookings.html', context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {
        'meta_title': f'{service.name} - Bluehawks Security Services',
        'meta_description': service.short_description,
        'meta_keywords': f'{service.name}, security services, Bluehawks, {service.name.lower()}',
        'service': service,
    }
    return render(request, 'mainwebsite/service_detail.html', context)

def robots_txt(request):
    content = """User-agent: *
Disallow: /admin/
Disallow: /static/admin/
Allow: /

Sitemap: https://bluehawks.com/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')
