from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import json
import logging

from .models import ContactSubmission, AirportBooking, Service
from .forms import ContactForm

# Set up logging
logger = logging.getLogger(__name__)


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

@csrf_protect
@require_http_methods(["GET", "POST"])
def contact(request):
    """
    Enhanced contact form view with comprehensive validation and error handling
    
    Features:
    - Django form validation with custom validators
    - CSRF protection
    - Rate limiting protection (basic)
    - IP address and user agent logging
    - Comprehensive error handling
    - Success/error messages
    - Database transaction safety
    """
    
    form = ContactForm()
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        # Get client information for logging
        client_ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        try:
            with transaction.atomic():  # Ensure database consistency
                
                # Basic rate limiting check (prevent spam)
                if is_rate_limited(request, client_ip):
                    messages.error(request, 
                        "Too many submissions from your IP address. Please wait a few minutes before trying again.")
                    logger.warning(f"Rate limited submission from IP: {client_ip}")
                    return redirect('contact')
                
                if form.is_valid():
                    # Create contact submission
                    contact_submission = form.save(commit=False)
                    
                    # Add metadata
                    contact_submission.ip_address = client_ip
                    contact_submission.user_agent = user_agent
                    
                    # Save to database
                    contact_submission.save()
                    
                    # Log successful submission
                    logger.info(f"Contact form submitted successfully: {contact_submission.name} ({contact_submission.email}) from IP: {client_ip}")
                    
                    # Send success message
                    messages.success(request, 
                        "Thank you for your message! We have received your inquiry and will get back to you within 24 hours.")
                    
                    # Optional: Send email notification to admin
                    # send_contact_notification(contact_submission)
                    
                    # Redirect to prevent re-submission on refresh
                    return redirect('contact')
                
                else:
                    # Form validation failed - log it but don't show alert messages
                    # Errors will be displayed inline within form fields
                    logger.warning(f"Contact form validation failed from IP: {client_ip}. Errors: {form.errors}")
        
        except ValidationError as e:
            # Handle validation errors
            logger.error(f"Validation error in contact form from IP: {client_ip}. Error: {str(e)}")
            messages.error(request, "There was a validation error with your submission. Please check your information and try again.")
        
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error in contact form from IP: {client_ip}. Error: {str(e)}")
            messages.error(request, "An unexpected error occurred. Please try again later or contact us directly.")
    
    # Prepare context for template
    context = {
        'meta_title': 'Contact Bluehawks Security Services - Get in Touch',
        'meta_description': 'Contact Bluehawks Security Services for professional security solutions, airport transportation, and security training. Located in Islamabad, Pakistan.',
        'meta_keywords': 'contact Bluehawks, security services contact, Islamabad security company',
        'form': form,
    }
    
    return render(request, 'mainwebsite/contact.html', context)


def get_client_ip(request):
    """Get the client's real IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_rate_limited(request, client_ip):
    """
    Basic rate limiting to prevent spam
    Allows maximum 3 submissions per IP per hour
    """
    from datetime import timedelta
    
    # Check submissions from this IP in the last hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_submissions = ContactSubmission.objects.filter(
        ip_address=client_ip,
        submitted_at__gte=one_hour_ago
    ).count()
    
    return recent_submissions >= 3  # Max 3 submissions per hour


# Optional: Email notification function (commented out for now)
"""
def send_contact_notification(contact_submission):
    '''
    Send email notification to admin when a new contact form is submitted
    '''
    from django.core.mail import send_mail
    from django.conf import settings
    
    subject = f"New Contact Form Submission from {contact_submission.name}"
    message = f'''
    A new contact form has been submitted:
    
    Name: {contact_submission.name}
    Email: {contact_submission.email}
    Phone: {contact_submission.phone or 'Not provided'}
    City: {contact_submission.city or 'Not provided'}
    Message: {contact_submission.message}
    
    Submitted at: {contact_submission.submitted_at}
    IP Address: {contact_submission.ip_address or 'Unknown'}
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_EMAIL],  # Add this to your settings
            fail_silently=False,
        )
        logger.info(f"Contact notification email sent for submission: {contact_submission.id}")
    except Exception as e:
        logger.error(f"Failed to send contact notification email: {str(e)}")
"""

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
