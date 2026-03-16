from django.shortcuts import render
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Donation
from .serializers import DonationSerializer, DonationStatsSerializer


@method_decorator(csrf_exempt, name='dispatch')
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        limit = int(request.query_params.get('limit', 10))
        donations = self.queryset[:limit]
        serializer = self.get_serializer(donations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_cause(self, request):
        cause = request.query_params.get('cause')
        if cause:
            donations = self.queryset.filter(cause__icontains=cause)
            serializer = self.get_serializer(donations, many=True)
            return Response(serializer.data)
        return Response({'error': 'Cause parameter required'}, status=400)


@api_view(['GET'])
def donation_stats(request):
    total_donations = Donation.objects.count()
    total_amount = Donation.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    

    by_cause = {}
    causes = Donation.objects.values('cause').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    for item in causes:
        by_cause[item['cause']] = {
            'amount': float(item['total']),
            'count': item['count']
        }
    
    by_coin = {}
    coins = Donation.objects.values('coin').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    for item in coins:
        by_coin[item['coin']] = {
            'amount': float(item['total']),
            'count': item['count']
        }
    
    return Response({
        'total_donations': total_donations,
        'total_amount': float(total_amount),
        'total_by_cause': by_cause,
        'total_by_coin': by_coin,
    })


@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'healthy',
        'message': 'BiToHelp API is running'
    })
