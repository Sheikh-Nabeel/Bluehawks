from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_contact_notification(contact):
    """
    Send email notification to admin about new contact submission
    """
    subject = f'New Contact Form Submission - {contact.name}'
    
    # Plain text version
    message = f"""
    New contact form submission received:
    
    Name: {contact.name}
    Email: {contact.email}
    Phone: {contact.phone or 'Not provided'}
    City: {contact.city or 'Not provided'}
    Message: {contact.message}
    Date: {contact.submitted_at}
    """
    
    # HTML version
    html_message = f"""
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong> {contact.name}</p>
    <p><strong>Email:</strong> {contact.email}</p>
    <p><strong>Phone:</strong> {contact.phone or 'Not provided'}</p>
    <p><strong>City:</strong> {contact.city or 'Not provided'}</p>
    <p><strong>Message:</strong></p>
    <p>{contact.message}</p>
    <p><strong>Date:</strong> {contact.submitted_at}</p>
    """
    
    try:
        send_mail(
            subject=subject,
            message=strip_tags(message),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to admin
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send contact notification: {e}")
        return False

def send_contact_confirmation(contact):
    """
    Send confirmation email to user who submitted contact form
    """
    subject = 'Thank you for contacting Bluehawks Security Services'
    
    # Plain text version
    message = f"""
    Dear {contact.name},
    
    Thank you for contacting Bluehawks Security Services. We have received your message and will get back to you as soon as possible.
    
    Your message details:
    Message: {contact.message}
    
    We appreciate your interest in our services.
    
    Best regards,
    Bluehawks Security Services Team
    """
    
    # HTML version
    html_message = f"""
    <h2>Thank you for contacting us!</h2>
    <p>Dear {contact.name},</p>
    <p>Thank you for contacting <strong>Bluehawks Security Services</strong>. We have received your message and will get back to you as soon as possible.</p>
    
    <h3>Your message details:</h3>
    <p><strong>Message:</strong> {contact.message}</p>
    
    <p>We appreciate your interest in our services.</p>
    
    <p>Best regards,<br>
    <strong>Bluehawks Security Services Team</strong></p>
    """
    
    try:
        send_mail(
            subject=subject,
            message=strip_tags(message),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[contact.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send contact confirmation: {e}")
        return False

def send_airport_booking_notification(booking):
    """
    Send email notification to admin about new airport booking
    """
    subject = f'New Airport Booking Request - {booking.name}'
    
    # Plain text version
    message = f"""
    New airport booking request received:
    
    Name: {booking.name}
    Email: {booking.email}
    Phone: {booking.phone}
    Number of Passengers: {booking.passengers or 'Not specified'}
    Pickup Airport: {booking.pickup_airport}
    Destination: {booking.destination}
    Travel Date: {booking.travel_date}
    Message: {booking.message or 'No additional message'}
    Date: {booking.submitted_at}
    """
    
    # HTML version
    html_message = f"""
    <h2>New Airport Booking Request</h2>
    <p><strong>Name:</strong> {booking.name}</p>
    <p><strong>Email:</strong> {booking.email}</p>
    <p><strong>Phone:</strong> {booking.phone}</p>
    <p><strong>Number of Passengers:</strong> {booking.passengers or 'Not specified'}</p>
    <p><strong>Pickup Airport:</strong> {booking.pickup_airport}</p>
    <p><strong>Destination:</strong> {booking.destination}</p>
    <p><strong>Travel Date:</strong> {booking.travel_date}</p>
    <p><strong>Message:</strong> {booking.message or 'No additional message'}</p>
    <p><strong>Date:</strong> {booking.submitted_at}</p>
    """
    
    try:
        send_mail(
            subject=subject,
            message=strip_tags(message),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to admin
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send airport booking notification: {e}")
        return False 