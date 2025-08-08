from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service

class ServiceSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Service.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    
    def items(self):
        return ['home', 'about', 'services', 'contact', 'clients', 'airport_bookings']
    
    def location(self, item):
        return reverse(item) 