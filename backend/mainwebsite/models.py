from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

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
