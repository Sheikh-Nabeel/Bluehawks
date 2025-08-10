from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import ContactSubmission, AirportBooking, Service

# Register your models here.

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    """Enhanced admin interface for Contact Submissions"""
    
    list_display = (
        "name", 
        "email", 
        "formatted_phone_display", 
        "city", 
        "short_message_display",
        "is_processed",
        "submitted_at"
    )
    
    list_display_links = ("name", "email")
    
    search_fields = (
        "name", 
        "email", 
        "phone", 
        "city", 
        "message",
        "ip_address"
    )
    
    list_filter = (
        "is_processed",
        "submitted_at",
        "city",
    )
    
    readonly_fields = (
        "submitted_at", 
        "ip_address", 
        "user_agent",
        "formatted_phone_display",
        "submission_details"
    )
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'city')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Processing', {
            'fields': ('is_processed', 'notes')
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('submission_details',),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = "submitted_at"
    ordering = ("-submitted_at",)
    
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    
    def formatted_phone_display(self, obj):
        """Display formatted phone number"""
        return obj.formatted_phone if obj.phone else "—"
    formatted_phone_display.short_description = "Phone"
    
    def short_message_display(self, obj):
        """Display truncated message"""
        return obj.short_message
    short_message_display.short_description = "Message Preview"
    
    def submission_details(self, obj):
        """Display detailed submission information"""
        if obj.pk:
            details = f"""
            <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">Submission ID:</td><td style="padding: 5px; border: 1px solid #ddd;">{obj.pk}</td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">Name:</td><td style="padding: 5px; border: 1px solid #ddd;">{obj.name}</td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">Email:</td><td style="padding: 5px; border: 1px solid #ddd;"><a href="mailto:{obj.email}">{obj.email}</a></td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">Phone:</td><td style="padding: 5px; border: 1px solid #ddd;">{obj.formatted_phone if obj.phone else 'Not provided'}</td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">City:</td><td style="padding: 5px; border: 1px solid #ddd;">{obj.city if obj.city else 'Not provided'}</td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">Submitted:</td><td style="padding: 5px; border: 1px solid #ddd;">{obj.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">IP Address:</td><td style="padding: 5px; border: 1px solid #ddd;">{obj.ip_address if obj.ip_address else 'Unknown'}</td></tr>
                <tr><td style="padding: 5px; border: 1px solid #ddd; font-weight: bold;">Processed:</td><td style="padding: 5px; border: 1px solid #ddd;">{'Yes' if obj.is_processed else 'No'}</td></tr>
            </table>
            <div style="margin-top: 15px;">
                <strong>Full Message:</strong><br>
                <div style="background: #f9f9f9; padding: 10px; border: 1px solid #ddd; margin-top: 5px; white-space: pre-wrap;">{obj.message}</div>
            </div>
            """
            return mark_safe(details)
        return "—"
    submission_details.short_description = "Submission Details"
    
    def mark_as_processed(self, request, queryset):
        """Mark selected submissions as processed"""
        updated = queryset.update(is_processed=True)
        self.message_user(request, f"{updated} submission(s) marked as processed.")
    mark_as_processed.short_description = "Mark selected submissions as processed"
    
    def mark_as_unprocessed(self, request, queryset):
        """Mark selected submissions as unprocessed"""
        updated = queryset.update(is_processed=False)
        self.message_user(request, f"{updated} submission(s) marked as unprocessed.")
    mark_as_unprocessed.short_description = "Mark selected submissions as unprocessed"

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
