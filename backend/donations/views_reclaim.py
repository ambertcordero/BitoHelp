from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Donation
from .serializers import DonationSerializer

@api_view(['POST'])
def record_reclaim(request):
    """
    Record a reclaim event for a donation. Expects JSON with:
    - donation_id: ID or txid of the donation
    - reclaim_txid: Transaction ID of the reclaim
    - reclaimed_amount: Amount reclaimed (in satoshis or BCH, optional)
    """
    donation_id = request.data.get('donation_id')
    reclaim_txid = request.data.get('reclaim_txid')
    reclaimed_amount = request.data.get('reclaimed_amount')
    if not donation_id or not reclaim_txid:
        return Response({'error': 'Missing donation_id or reclaim_txid'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        donation = Donation.objects.get(id=donation_id)
    except Donation.DoesNotExist:
        try:
            donation = Donation.objects.get(txid=donation_id)
        except Donation.DoesNotExist:
            return Response({'error': 'Donation not found'}, status=status.HTTP_404_NOT_FOUND)
    donation.reclaim_txid = reclaim_txid
    # Enforce txid is always set (if missing, set to reclaim_txid as fallback)
    if not donation.txid:
        donation.txid = reclaim_txid
    if reclaimed_amount:
        donation.amount = reclaimed_amount
    donation.save()
    return Response(DonationSerializer(donation).data, status=status.HTTP_200_OK)
