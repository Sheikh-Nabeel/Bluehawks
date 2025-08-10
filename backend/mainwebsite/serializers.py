from rest_framework import serializers
from .models import ContactSubmission, AirportBooking, Service

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'city', 'message']
        
    def create(self, validated_data):
        return ContactSubmission.objects.create(**validated_data)

class AirportBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirportBooking
        fields = ['name', 'email', 'phone', 'passengers', 'pickup_airport', 'destination', 'travel_date', 'message']
        
    def create(self, validated_data):
        return AirportBooking.objects.create(**validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'description', 'short_description', 'image', 'icon', 'is_active', 'created_at']


