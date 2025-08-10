from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import ContactSubmission, AirportBooking, Service
from .serializers import ContactSubmissionSerializer, AirportBookingSerializer, ServiceSerializer
from .email_utils import send_contact_notification, send_airport_booking_notification, send_contact_confirmation

@api_view(['POST'])
def contact_submission(request):
    """API endpoint for contact form submissions"""
    serializer = ContactSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        contact = serializer.save()
        
        # Send email notifications
        try:
            # Send notification to admin
            send_contact_notification(contact)
            # Send confirmation to user
            send_contact_confirmation(contact)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Email notification failed: {e}")
        
        return Response({
            'message': 'Your message has been sent successfully!'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Please check your input and try again.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def airport_booking(request):
    """API endpoint for airport booking submissions"""
    serializer = AirportBookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save()
        
        # Send email notification
        try:
            send_airport_booking_notification(booking)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Email notification failed: {e}")
        
        return Response({
            'message': 'Your airport booking request has been sent successfully!'
        }, status=status.HTTP_201_CREATED)
    return Response({
        'message': 'Please check your input and try again.',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

class ServiceViewSet(ReadOnlyModelViewSet):
    """API endpoint for services"""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
