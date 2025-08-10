from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'services', api_views.ServiceViewSet)

urlpatterns = [
    path('contact/', api_views.contact_submission, name='api_contact'),
    path('airport-booking/', api_views.airport_booking, name='api_airport_booking'),
    path('', include(router.urls)),
]


