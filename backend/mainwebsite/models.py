from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
import re

# Create your models here.

class ContactSubmission(models.Model):
    """
    Contact form submission model with comprehensive validation
    Stores contact form submissions from the website
    """
    
    # Validators
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]+$',
        message='Name can only contain letters and spaces.',
        code='invalid_name'
    )
    
    city_validator = RegexValidator(
        regex=r'^[a-zA-Z\s]+$',
        message='City name can only contain letters and spaces.',
        code='invalid_city'
    )
    
    phone_validator = RegexValidator(
        regex=r'^(\+92|92|0)?[0-9\s\-\(\)]{10,20}$',
        message='Please enter a valid Pakistan phone number.',
        code='invalid_phone'
    )
    
    # Fields
    name = models.CharField(
        max_length=50,
        validators=[
            name_validator,
            MinLengthValidator(2, message='Name must be at least 2 characters long.'),
            MaxLengthValidator(50, message='Name cannot exceed 50 characters.')
        ],
        help_text='Full name (2-50 characters, letters and spaces only)'
    )
    
    email = models.EmailField(
        max_length=100,
        help_text='Valid email address (max 100 characters)'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[phone_validator],
        help_text='Pakistan phone number (optional)'
    )
    
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[
            city_validator,
            MinLengthValidator(2, message='City name must be at least 2 characters long.')
        ],
        help_text='City name (optional, letters and spaces only)'
    )
    
    message = models.TextField(
        validators=[
            MinLengthValidator(10, message='Message must be at least 10 characters long.'),
            MaxLengthValidator(1000, message='Message cannot exceed 1000 characters.')
        ],
        help_text='Your message (10-1000 characters)'
    )
    
    # Metadata fields
    submitted_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True, help_text='IP address of submitter')
    user_agent = models.TextField(blank=True, null=True, help_text='Browser user agent')
    is_processed = models.BooleanField(default=False, help_text='Has this submission been processed?')
    notes = models.TextField(blank=True, null=True, help_text='Admin notes about this submission')
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
        indexes = [
            models.Index(fields=['-submitted_at']),
            models.Index(fields=['email']),
            models.Index(fields=['is_processed']),
        ]
    
    def clean(self):
        """Additional model-level validation"""
        super().clean()
        
        # Validate name
        if self.name:
            self.name = self.name.strip()
            if not re.match(r'^[a-zA-Z\s]+$', self.name):
                raise ValidationError({'name': 'Name can only contain letters and spaces.'})
        
        # Validate email
        if self.email:
            self.email = self.email.strip().lower()
            if len(self.email) > 100:
                raise ValidationError({'email': 'Email address is too long.'})
        
        # Validate phone (if provided)
        if self.phone:
            self.phone = self.phone.strip()
            # Remove formatting characters for validation
            clean_phone = re.sub(r'[\s\-\(\)]', '', self.phone)
            if not re.match(r'^(\+92|92|0)?[0-9]{10,11}$', clean_phone):
                raise ValidationError({'phone': 'Please enter a valid Pakistan phone number.'})
        
        # Validate city (if provided)
        if self.city:
            self.city = self.city.strip()
            if not re.match(r'^[a-zA-Z\s]+$', self.city):
                raise ValidationError({'city': 'City name can only contain letters and spaces.'})
        
        # Validate message
        if self.message:
            self.message = self.message.strip()
            # Basic spam detection
            spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'click here', 'make money']
            message_lower = self.message.lower()
            
            for keyword in spam_keywords:
                if keyword in message_lower:
                    raise ValidationError({'message': 'Message contains inappropriate content.'})
    
    def save(self, *args, **kwargs):
        """Override save to clean and format data"""
        # Clean and format data before saving
        if self.name:
            self.name = self.name.strip().title()
        
        if self.email:
            self.email = self.email.strip().lower()
        
        if self.phone:
            self.phone = self.phone.strip()
        
        if self.city:
            self.city = self.city.strip().title()
        
        if self.message:
            self.message = self.message.strip()
        
        # Call clean method
        self.full_clean()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def formatted_phone(self):
        """Return formatted phone number"""
        if self.phone:
            # Basic formatting for display
            clean_phone = re.sub(r'[\s\-\(\)]', '', self.phone)
            if clean_phone.startswith('+92'):
                return f"+92 {clean_phone[3:5]} {clean_phone[5:8]} {clean_phone[8:]}"
            elif clean_phone.startswith('92'):
                return f"+92 {clean_phone[2:4]} {clean_phone[4:7]} {clean_phone[7:]}"
            elif clean_phone.startswith('0'):
                return f"{clean_phone[:4]} {clean_phone[4:7]} {clean_phone[7:]}"
        return self.phone
    
    @property
    def short_message(self):
        """Return truncated message for admin display"""
        if len(self.message) > 100:
            return f"{self.message[:100]}..."
        return self.message

class AirportBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    passengers = models.CharField(max_length=10, blank=True)
    pickup_airport = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    travel_date = models.DateField()
    message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.pickup_airport} to {self.destination} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"

class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    image = models.CharField(max_length=200, blank=True)  # For static image paths
    icon = models.CharField(max_length=50, blank=True)  # For FontAwesome icons
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name
