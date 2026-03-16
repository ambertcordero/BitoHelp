from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NonprofitViewSet

router = DefaultRouter()
router.register(r'nonprofits', NonprofitViewSet, basename='nonprofit')

urlpatterns = [
    path('', include(router.urls)),
]
