from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Nonprofit
from .serializers import NonprofitSerializer, NonprofitListSerializer

class NonprofitViewSet(viewsets.ModelViewSet):
    queryset = Nonprofit.objects.filter(active=True)
    serializer_class = NonprofitSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'verified']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'total_donations']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NonprofitListSerializer
        return NonprofitSerializer
    
    @action(detail=False, methods=['get'])
    def verified(self, request):
        nonprofits = self.queryset.filter(verified=True)
        serializer = self.get_serializer(nonprofits, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def donations(self, request, pk=None):
        nonprofit = self.get_object()
        from donations.models import Donation
        from donations.serializers import DonationSerializer
        
        donations = Donation.objects.filter(nonprofit=nonprofit)
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)
