from django.shortcuts import render
from django.db.models import Sum, Count
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Donation
from .serializers import DonationSerializer, DonationStatsSerializer
from users.models import WalletUser
import re
import time

TXID_PATTERN = re.compile(r'^[A-Fa-f0-9]{64}$')


@method_decorator(csrf_exempt, name='dispatch')
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create to retry on database lock and link wallet user"""
        txid = (request.data.get('txid') or '').strip()
        if not TXID_PATTERN.fullmatch(txid):
            return Response(
                {'error': f'Invalid txid format: must be a 64-character hex hash, got "{txid[:80]}"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        max_retries = 5
        for attempt in range(max_retries):
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                with transaction.atomic():
                    # Auto-link wallet user if wallet_address provided
                    wallet_addr = request.data.get('wallet_address', '').lower().strip()
                    extra_kwargs = {}
                    if wallet_addr:
                        extra_kwargs['wallet_address'] = wallet_addr
                        wallet_user = WalletUser.objects.filter(wallet_address=wallet_addr).first()
                        if wallet_user:
                            extra_kwargs['wallet_user'] = wallet_user
                    self.perform_create(serializer, **extra_kwargs)
                
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as e:
                error_msg = str(e).lower()
                is_lock_error = 'database is locked' in error_msg or 'locked' in error_msg
                if is_lock_error and attempt < max_retries - 1:
                    time.sleep(0.2 * (attempt + 1))  # Exponential backoff
                    continue
                raise
        
        return Response({'error': 'Database temporarily unavailable'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def perform_create(self, serializer, **extra_kwargs):
        serializer.save(**extra_kwargs)

    def list(self, request, *args, **kwargs):
        """Optionally filter donations by wallet address."""
        wallet = request.query_params.get('wallet', '').lower().strip()
        queryset = self.get_queryset()
        if wallet:
            queryset = queryset.filter(wallet_address=wallet)
        limit = request.query_params.get('limit')
        if limit:
            queryset = queryset[:int(limit)]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
    """Get donation statistics"""
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
        'message': 'CrypToCare API is running'
    })
