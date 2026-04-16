from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import WalletUser
from .serializers import WalletUserSerializer, WalletConnectSerializer
from donations.models import Donation
from donations.serializers import DonationSerializer
from payouts.models import PayoutApproval
from payouts.serializers import PayoutApprovalSerializer


@api_view(['POST'])
def wallet_connect(request):
    """
    Update metadata for an existing wallet user (chain, balance, etc).
    Does NOT create a new WalletUser — that only happens on first donation.
    POST /api/users/connect/
    """
    serializer = WalletConnectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    raw_address = serializer.validated_data['wallet_address'].lower().strip()
    if not raw_address:
        return Response({'error': 'wallet_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = WalletUser.objects.get(wallet_address=raw_address)
    except WalletUser.DoesNotExist:
        return Response({'exists': False, 'wallet_address': raw_address}, status=status.HTTP_200_OK)

    chain = serializer.validated_data.get('chain', '').strip()
    namespace = serializer.validated_data.get('namespace', '').strip()
    balance = serializer.validated_data.get('balance', 0)
    symbol = serializer.validated_data.get('symbol', '').strip()

    update_fields = ['last_connected_at']
    user.last_connected_at = timezone.now()

    if chain:
        user.chain = chain
        update_fields.append('chain')
    if namespace:
        user.namespace = namespace
        update_fields.append('namespace')
    if balance:
        user.balance = balance
        update_fields.append('balance')
    if symbol:
        user.symbol = symbol
        update_fields.append('symbol')

    user.save(update_fields=update_fields)
    return Response(WalletUserSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def wallet_role(request, wallet_address):
    """
    Check the role of a wallet address.
    Returns: { role: 'nonprofit' | 'donor' | 'new' }
    GET /api/users/<wallet_address>/role/
    """
    from nonprofits.models import Nonprofit

    addr = wallet_address.lower().strip()
    if not addr:
        return Response({'error': 'wallet_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    if Nonprofit.objects.filter(bch_address__iexact=addr).exists():
        return Response({'role': 'nonprofit', 'wallet_address': addr})

    if WalletUser.objects.filter(wallet_address=addr).exists():
        return Response({'role': 'donor', 'wallet_address': addr})

    return Response({'role': 'new', 'wallet_address': addr})


@api_view(['GET'])
def wallet_profile(request, wallet_address):
    """
    Get full donor profile for a wallet: user info + donations + stats.
    GET /api/users/<wallet_address>/profile/
    """
    addr = wallet_address.lower().strip()
    if not addr:
        return Response({'error': 'wallet_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = WalletUser.objects.get(wallet_address=addr)
    except WalletUser.DoesNotExist:
        user = None

    donations = Donation.objects.filter(wallet_address=addr).order_by('-timestamp')
    donation_data = DonationSerializer(donations, many=True).data

    total_donated = sum(float(d.amount) for d in donations)
    donation_count = donations.count()

    return Response({
        'user': WalletUserSerializer(user).data if user else None,
        'donations': donation_data,
        'stats': {
            'total_donated': total_donated,
            'donation_count': donation_count,
        },
    })


@api_view(['GET'])
def wallet_donations(request, wallet_address):
    """
    Get donations for a specific wallet.
    GET /api/users/<wallet_address>/donations/
    """
    addr = wallet_address.lower().strip()
    if not addr:
        return Response({'error': 'wallet_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    limit = int(request.query_params.get('limit', 50))
    donations = Donation.objects.filter(wallet_address=addr).order_by('-timestamp')[:limit]
    return Response(DonationSerializer(donations, many=True).data)


@api_view(['GET'])
def wallet_users_list(request):
    """
    List all wallet users.
    GET /api/users/
    """
    users = WalletUser.objects.all().order_by('-created_at')
    return Response(WalletUserSerializer(users, many=True).data)


@api_view(['GET'])
def wallet_user_detail(request, pk):
    """
    Get a single wallet user by ID.
    GET /api/users/<id>/
    """
    try:
        user = WalletUser.objects.get(pk=pk)
    except WalletUser.DoesNotExist:
        return Response({'error': 'Wallet user not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(WalletUserSerializer(user).data)


@api_view(['GET'])
def wallet_user_activities(request, pk):
    """
    Full activity history for a wallet user (donations + payout approvals),
    merged into a single timeline sorted newest first.
    GET /api/users/<id>/activities/
    """
    try:
        user = WalletUser.objects.get(pk=pk)
    except WalletUser.DoesNotExist:
        return Response({'error': 'Wallet user not found'}, status=status.HTTP_404_NOT_FOUND)

    addr = user.wallet_address

    # Donations for this wallet
    donations = Donation.objects.filter(wallet_address=addr).order_by('-timestamp')
    donation_data = DonationSerializer(donations, many=True).data

    # Payout approvals linked via donation FK
    donation_ids = list(donations.values_list('id', flat=True))
    payout_approvals = (
        PayoutApproval.objects
        .filter(donation_id__in=donation_ids)
        .order_by('-created_at')
    )
    payout_data = PayoutApprovalSerializer(payout_approvals, many=True).data

    # Build merged activity timeline
    activities = []
    for d in donation_data:
        activities.append({
            'type': 'donation',
            'timestamp': d.get('timestamp'),
            'data': d,
        })
    for p in payout_data:
        activities.append({
            'type': 'payout_approval',
            'timestamp': p.get('created_at'),
            'data': p,
        })
    activities.sort(key=lambda a: a.get('timestamp') or '', reverse=True)

    return Response({
        'user': WalletUserSerializer(user).data,
        'donations': donation_data,
        'payout_approvals': payout_data,
        'activities': activities,
        'stats': {
            'total_donated': float(sum(d.amount for d in donations)),
            'donation_count': donations.count(),
            'payout_count': payout_approvals.count(),
        },
    })
