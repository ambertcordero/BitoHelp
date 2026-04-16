from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationViewSet, donation_stats, health_check
from .views_reclaim import record_reclaim

router = DefaultRouter()
router.register(r'donations', DonationViewSet, basename='donation')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', donation_stats, name='donation-stats'),
    path('health/', health_check, name='health-check'),
    path('reclaim/', record_reclaim, name='donation-reclaim'),
]
