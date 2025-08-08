from django.contrib import admin
from .models import ContactSubmission, AirportBooking, Service

# Register your models here.

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "city", "submitted_at")
    search_fields = ("name", "email", "phone", "city", "message")
    list_filter = ("submitted_at",)
    readonly_fields = ("submitted_at",)

@admin.register(AirportBooking)
class AirportBookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "pickup_airport", "destination", "travel_date", "submitted_at")
    search_fields = ("name", "email", "phone", "pickup_airport", "destination")
    list_filter = ("submitted_at", "travel_date", "pickup_airport")
    readonly_fields = ("submitted_at",)
    date_hierarchy = "travel_date"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "description", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
