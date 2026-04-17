from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Vault, WithdrawalCycle
from .serializers import (
    VaultListSerializer, VaultDetailSerializer,
    VaultCreateSerializer, VaultUpdateSerializer,
    WithdrawalCycleSerializer,
)
from users.models import WalletUser
from nonprofits.models import Nonprofit


@api_view(['GET', 'POST'])
def vault_list_create(request):
    """
    GET  /api/vaults/?wallet_address=X&network=Y&status=Z
    POST /api/vaults/
    """
    if request.method == 'GET':
        qs = Vault.objects.all()
        wallet_address = request.query_params.get('wallet_address', '').lower().strip()
        network = request.query_params.get('network', '').strip()
        vault_status = request.query_params.get('status', '').strip()

        if wallet_address:
            qs = qs.filter(funder_address=wallet_address)
        if network:
            qs = qs.filter(network=network)
        if vault_status:
            qs = qs.filter(status=vault_status)

        return Response(VaultListSerializer(qs, many=True).data)

    # POST
    serializer = VaultCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Link wallet user if possible
    funder = serializer.validated_data.get('funder_address', '').lower().strip()
    wallet_user = None
    if funder:
        wallet_user = WalletUser.objects.filter(wallet_address=funder).first()

    vault = serializer.save(wallet_user=wallet_user)

    # Auto-populate recipient_name from Nonprofit table if not provided
    if not vault.recipient_name and vault.recipient_address:
        np = Nonprofit.objects.filter(bch_address=vault.recipient_address).first()
        if np:
            vault.recipient_name = np.name
            vault.save(update_fields=['recipient_name'])

    return Response(VaultDetailSerializer(vault).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH'])
def vault_detail(request, pk):
    """
    GET   /api/vaults/<id>/
    PATCH /api/vaults/<id>/
    """
    try:
        vault = Vault.objects.get(pk=pk)
    except Vault.DoesNotExist:
        return Response({'error': 'Vault not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(VaultDetailSerializer(vault).data)

    # PATCH
    serializer = VaultUpdateSerializer(vault, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(VaultDetailSerializer(vault).data)


@api_view(['GET'])
def vault_by_donation_id(request, donation_id_ref):
    """
    GET /api/vaults/by-donation/<donation_id_ref>/
    Convenience lookup by frontend-generated donation ID.
    """
    try:
        vault = Vault.objects.get(donation_id_ref=donation_id_ref)
    except Vault.DoesNotExist:
        return Response({'error': 'Vault not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(VaultDetailSerializer(vault).data)


@api_view(['POST'])
def vault_record_cycle(request, pk):
    """
    POST /api/vaults/<id>/cycles/
    Record a completed withdrawal cycle.
    """
    try:
        vault = Vault.objects.get(pk=pk)
    except Vault.DoesNotExist:
        return Response({'error': 'Vault not found'}, status=status.HTTP_404_NOT_FOUND)

    cycle_number = request.data.get('cycle_number')
    txid = request.data.get('txid', '').strip()
    amount_satoshis = request.data.get('amount_satoshis', 0)
    drained = request.data.get('drained', False)

    if not cycle_number or not txid:
        return Response({'error': 'cycle_number and txid are required'},
                        status=status.HTTP_400_BAD_REQUEST)

    cycle, created = WithdrawalCycle.objects.get_or_create(
        vault=vault,
        cycle_number=cycle_number,
        defaults={
            'txid': txid,
            'amount_satoshis': amount_satoshis,
            'drained': drained,
        },
    )

    if not created:
        # Idempotent: update txid if it changed
        if cycle.txid != txid:
            cycle.txid = txid
            cycle.amount_satoshis = amount_satoshis
            cycle.drained = drained
            cycle.save()

    # Update parent vault state
    vault.cycles_completed = vault.withdrawal_cycles.count()
    vault.last_withdraw_txid = txid
    vault.last_withdraw_at = timezone.now()
    if drained or vault.cycles_completed >= vault.total_cycles:
        vault.status = 'drained'
    elif vault.status in ('active', 'funded'):
        vault.status = 'withdrawing'
    vault.save(update_fields=[
        'cycles_completed', 'last_withdraw_txid', 'last_withdraw_at', 'status', 'updated_at',
    ])

    return Response(WithdrawalCycleSerializer(cycle).data,
                    status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
