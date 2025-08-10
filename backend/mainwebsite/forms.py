from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    """
    Contact form with comprehensive validation for:
    - Name (required): 2-50 characters, letters and spaces only
    - Email (required): Valid email format, max 100 characters
    - Phone (optional): Pakistan phone number format validation
    - City (optional): 2-50 characters, letters and spaces only
    - Message (required): 10-1000 characters
    """
    
    # Custom validators
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
        message='Please enter a valid Pakistan phone number (e.g., 03001234567 or +923001234567).',
        code='invalid_phone'
    )
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'city', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'required': True,
                'id': 'name',
                'maxlength': '50'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'required': True,
                'id': 'email',
                'maxlength': '100'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'id': 'phone',
                'maxlength': '20'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'id': 'city',
                'maxlength': '50'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'required': True,
                'id': 'message',
                'rows': 5,
                'maxlength': '1000'
            }),
        }
        labels = {
            'name': 'Name *',
            'email': 'Email Address *',
            'phone': 'Phone',
            'city': 'City',
            'message': 'Message *',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply custom validators
        self.fields['name'].validators = [self.name_validator]
        self.fields['city'].validators = [self.city_validator]
        self.fields['phone'].validators = [self.phone_validator]
        
        # Set field requirements
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = False
        self.fields['city'].required = False
        self.fields['message'].required = True
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name')
        
        if name is None:
            name = ''
        else:
            name = name.strip()
        
        if not name:
            raise ValidationError('Name is required.')
        
        if len(name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
        if len(name) > 50:
            raise ValidationError('Name cannot exceed 50 characters.')
        
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationError('Name can only contain letters and spaces.')
        
        return name
    
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')
        
        if email is None:
            email = ''
        else:
            email = email.strip().lower()
        
        if not email:
            raise ValidationError('Email address is required.')
        
        if len(email) > 100:
            raise ValidationError('Email address is too long.')
        
        # Additional email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError('Please enter a valid email address (e.g., user@example.com).')
        
        return email
    
    def clean_phone(self):
        """Validate phone field (optional but must be valid if provided)"""
        phone = self.cleaned_data.get('phone')
        
        if phone is None:
            return ''
        
        phone = phone.strip()
        
        if phone:  # Only validate if phone is provided and not empty
            if len(phone) > 20:
                raise ValidationError('Phone number is too long.')
            
            # Remove common formatting characters for validation
            clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
            
            # Pakistan phone number validation
            if not re.match(r'^(\+92|92|0)?[0-9]{10,11}$', clean_phone):
                raise ValidationError('Please enter a valid Pakistan phone number (e.g., 03001234567 or +923001234567).')
        
        return phone
    
    def clean_city(self):
        """Validate city field (optional but must be valid if provided)"""
        city = self.cleaned_data.get('city')
        
        if city is None:
            return ''
        
        city = city.strip()
        
        if city:  # Only validate if city is provided and not empty
            if len(city) < 2:
                raise ValidationError('City name must be at least 2 characters long.')
            
            if len(city) > 50:
                raise ValidationError('City name cannot exceed 50 characters.')
            
            if not re.match(r'^[a-zA-Z\s]+$', city):
                raise ValidationError('City name can only contain letters and spaces.')
        
        return city
    
    def clean_message(self):
        """Validate message field"""
        message = self.cleaned_data.get('message')
        
        if message is None:
            message = ''
        else:
            message = message.strip()
        
        if not message:
            raise ValidationError('Message is required.')
        
        if len(message) < 10:
            raise ValidationError('Message must be at least 10 characters long.')
        
        if len(message) > 1000:
            raise ValidationError('Message cannot exceed 1000 characters.')
        
        return message
    
    def clean(self):
        """Additional form-wide validation"""
        cleaned_data = super().clean()
        
        # Check for spam patterns (basic implementation)
        message = cleaned_data.get('message', '')
        email = cleaned_data.get('email', '')
        
        # Basic spam detection
        spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'click here', 'make money']
        message_lower = message.lower()
        
        for keyword in spam_keywords:
            if keyword in message_lower:
                raise ValidationError('Your message contains inappropriate content. Please revise and try again.')
        
        # Check for suspicious repeated characters
        if re.search(r'(.)\1{10,}', message):  # More than 10 repeated characters
            raise ValidationError('Your message contains invalid content. Please revise and try again.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Override save to add additional processing"""
        instance = super().save(commit=False)
        
        # Clean and format data before saving
        if instance.name:
            instance.name = instance.name.strip().title()
        
        if instance.email:
            instance.email = instance.email.strip().lower()
        
        if instance.phone:
            instance.phone = instance.phone.strip()
        
        if instance.city:
            instance.city = instance.city.strip().title()
        
        if instance.message:
            instance.message = instance.message.strip()
        
        if commit:
            instance.save()
        
        return instance
