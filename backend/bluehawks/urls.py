"""
URL configuration for bluehawks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from mainwebsite.views import home, about, services, contact, clients, airport_bookings, service_detail, robots_txt
from mainwebsite.sitemaps import ServiceSitemap, StaticViewSitemap

sitemaps = {
    'services': ServiceSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('service/<slug:slug>/', service_detail, name='service_detail'),
    path('contact/', contact, name='contact'),
    path('clients/', clients, name='clients'),
    path('airport-bookings/', airport_bookings, name='airport_bookings'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('admin/', admin.site.urls),
]
