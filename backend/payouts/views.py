import logging
import re
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import PayoutApproval, PayoutAuditLog
from .models import PayoutApproval, PayoutAuditLog
from .serializers import PayoutApprovalSerializer, PayoutApprovalListSerializer, PayoutAuditLogSerializer
from .services import create_pending_approval, send_approval_email, process_approval, mark_executed, mark_failed, refresh_and_send, send_reclaim_warning_email

logger = logging.getLogger(__name__)


TXID_PATTERN = re.compile(r'^[A-Fa-f0-9]{64}$')


# ── Gmail ConfirmAction callback ──────────────────────────────────────

@csrf_exempt
def gmail_approve(request, token):
    """
    Process a Gmail one-click action approval.
    - POST: Gmail's HttpActionHandler callback (no body, token in path)
    - GET:  Browser click from the email link — shows a confirmation page
    """
    if request.method not in ('GET', 'POST'):
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    ip = _get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')

    approval, error = process_approval(token, ip_address=ip, user_agent=ua)

    if request.method == 'GET':
        if error:
            return _approval_html_response('Approval Failed', error, success=False)
        return _approval_html_response(
            'Payout Approved!',
            f'Your payout of {approval.payout_amount_satoshis} sats to '
            f'{approval.recipient_address} has been approved. '
            f'The withdrawal will be executed shortly.',
            success=True,
        )

    # POST — JSON response for Gmail action handler
    if error:
        status_code = 410 if approval and approval.is_expired else 400
        return JsonResponse({'ok': False, 'error': error}, status=status_code)

    return JsonResponse({
        'ok': True,
        'message': 'Payout approved! The withdrawal will be executed shortly.',
        'approval_id': approval.id,
        'status': approval.status,
    })


# ── REST API endpoints ────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def request_approval(request):
    """
    Frontend calls this to create a pending approval and trigger the email.
    """
    data = request.data
    # donor_email is only strictly required for inbox_approval mode
    payout_mode = data.get('payout_mode', 'smart')
    required = ['donation_id', 'recipient_address', 'payout_amount_satoshis']
    if payout_mode == 'inbox_approval':
        required.append('donor_email')
    missing = [f for f in required if not data.get(f)]
    if missing:
        return Response({'error': f'Missing fields: {", ".join(missing)}'}, status=400)

    vault_bal = data.get('vault_balance_satoshis')

    # Parse optional due_at ISO string from frontend
    due_at = None
    due_at_str = data.get('due_at')
    if due_at_str:
        from django.utils.dateparse import parse_datetime
        due_at = parse_datetime(due_at_str)

    approval, raw_token = create_pending_approval(
        donation_id=data['donation_id'],
        donor_email=data.get('donor_email', ''),
        donor_name=data.get('donor_name', ''),
        recipient_address=data['recipient_address'],
        vault_address=data.get('vault_address', ''),
        payout_amount_satoshis=int(data['payout_amount_satoshis']),
        coin=data.get('coin', 'BCH'),
        interval_label=data.get('interval_label', ''),
        interval_blocks=int(data.get('interval_blocks', 1)),
        cycle_number=int(data.get('cycle_number', 1)),
        total_cycles=int(data.get('total_cycles', 1)),
        vault_balance_satoshis=int(vault_bal) if vault_bal is not None else None,
        due_at=due_at,
    )

    # Link the donation FK so the dashboard can filter by nonprofit_id.
    # Try matching by vault address (stored as Donation.contract) first,
    # then fall back to the donation_ref string if it looks like a numeric DB ID.
    if approval.donation_id is None:
        from donations.models import Donation
        vault_address = data.get('vault_address', '')
        linked = None
        if vault_address:
            linked = Donation.objects.filter(contract=vault_address).first()
        if linked is None:
            ref = data.get('donation_id', '')
            if ref and str(ref).isdigit():
                linked = Donation.objects.filter(pk=int(ref)).first()
        if linked is not None:
            approval.donation = linked
            approval.save(update_fields=['donation'])

    if raw_token and payout_mode == 'inbox_approval':
        try:
            send_approval_email(approval, raw_token)
        except Exception as exc:
            return Response({
                'error': f'Approval created but email failed: {exc}',
                'approval_id': approval.id,
            }, status=500)

    serializer = PayoutApprovalSerializer(approval)
    return Response(serializer.data, status=201 if raw_token else 200)


@api_view(['GET'])
@permission_classes([AllowAny])
def approval_status(request, pk):
    """Check the current status of a payout approval."""
    try:
        approval = PayoutApproval.objects.get(pk=pk)
    except PayoutApproval.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    serializer = PayoutApprovalSerializer(approval)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_approvals(request):
    """
    List payout approvals, optionally filtered by donation_id or status.
    """
    qs = PayoutApproval.objects.all()

    donation_id = request.query_params.get('donation_id')
    if donation_id:
        qs = qs.filter(donation_ref=donation_id)

    nonprofit_id = request.query_params.get('nonprofit_id')
    if nonprofit_id:
        from django.db.models import Q
        from donations.models import Donation
        # Primary: match via donation FK (preferred, set at creation time)
        # Fallback: match via vault_address → Donation.contract for records created
        # before the FK-linking fix was deployed
        try:
            nid = int(nonprofit_id)
        except (TypeError, ValueError):
            nid = None
        if nid is not None:
            matching_contracts = Donation.objects.filter(nonprofit_id=nid).values_list('contract', flat=True)
            qs = qs.filter(
                Q(donation__nonprofit_id=nid) |
                Q(vault_address__in=[c for c in matching_contracts if c])
            ).distinct()
        else:
            qs = qs.none()

    status = request.query_params.get('status')
    if status:
        qs = qs.filter(status=status)

    serializer = PayoutApprovalListSerializer(qs[:100], many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def approval_audit_log(request, pk):
    """Get the audit log for a specific payout approval."""
    try:
        approval = PayoutApproval.objects.get(pk=pk)
    except PayoutApproval.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    logs = approval.audit_logs.all()
    serializer = PayoutAuditLogSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def report_execution(request, pk):
    """Frontend reports that a payout was successfully executed on-chain."""
    try:
        approval = PayoutApproval.objects.get(pk=pk)
    except PayoutApproval.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    txid = (request.data.get('txid', '') or '').strip()

    if txid and not TXID_PATTERN.fullmatch(txid):
        return Response(
            {'error': 'txid must be a 64-character hexadecimal blockchain transaction ID.'},
            status=400,
        )

    if txid:
        txid = txid.lower()

    if approval.status == 'executed':
        if txid and not approval.txid:
            approval.txid = txid
            approval.save(update_fields=['txid', 'updated_at'])
            PayoutAuditLog.objects.create(
                payout_approval=approval,
                action=PayoutAuditLog.Action.EXECUTED,
                detail=f'Updated missing txid for already-executed payout: txid={txid}',
            )
            serializer = PayoutApprovalSerializer(approval)
            return Response(serializer.data)
        return Response({'message': 'Already executed', 'txid': approval.txid})

    mark_executed(approval, txid)

    # Auto-schedule the next cycle if more remain
    if approval.cycle_number < approval.total_cycles:
        from datetime import timedelta
        from django.utils import timezone
        next_due = approval.executed_at + timedelta(minutes=approval.interval_blocks * 10)
        try:
            next_approval, _ = create_pending_approval(
                donation_id=approval.donation_ref,
                donor_email=approval.donor_email,
                donor_name=approval.donor_name,
                recipient_address=approval.recipient_address,
                vault_address=approval.vault_address,
                payout_amount_satoshis=approval.payout_amount_satoshis,
                coin=approval.coin,
                interval_label=approval.interval_label,
                interval_blocks=approval.interval_blocks,
                cycle_number=approval.cycle_number + 1,
                total_cycles=approval.total_cycles,
                due_at=next_due,
            )
            if approval.donation_id and next_approval:
                next_approval.donation_id = approval.donation_id
                next_approval.save(update_fields=['donation'])
        except Exception as exc:
            logger.warning('Failed to create next cycle approval: %s', exc)

    serializer = PayoutApprovalSerializer(approval)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def report_execution_by_vault(request):
    """
    Smart mode reports a successful on-chain withdrawal by vault address + cycle.
    Finds the matching PayoutApproval and marks it executed with the real txid.
    """
    data = request.data
    vault_address = (data.get('vault_address', '') or '').strip()
    cycle_number = data.get('cycle_number')
    txid = (data.get('txid', '') or '').strip()

    if not vault_address or cycle_number is None:
        return Response({'error': 'vault_address and cycle_number are required'}, status=400)

    if txid and not TXID_PATTERN.fullmatch(txid):
        return Response(
            {'error': 'txid must be a 64-character hexadecimal blockchain transaction ID.'},
            status=400,
        )
    if txid:
        txid = txid.lower()

    try:
        cycle_number = int(cycle_number)
    except (TypeError, ValueError):
        return Response({'error': 'cycle_number must be an integer'}, status=400)

    # Find matching approval: prefer pending, then executed-without-txid,
    # then any executed record (so cached txids can always overwrite bad data).
    approval = (
        PayoutApproval.objects.filter(
            vault_address=vault_address,
            cycle_number=cycle_number,
            status=PayoutApproval.Status.PENDING,
        ).first()
    )
    if not approval:
        approval = (
            PayoutApproval.objects.filter(
                vault_address=vault_address,
                cycle_number=cycle_number,
                status=PayoutApproval.Status.EXECUTED,
                txid='',
            ).first()
        )
    if not approval:
        # Last resort: find any executed record (even with a different txid)
        approval = (
            PayoutApproval.objects.filter(
                vault_address=vault_address,
                cycle_number=cycle_number,
                status=PayoutApproval.Status.EXECUTED,
            ).first()
        )

    if not approval:
        return Response({'error': 'No matching approval found'}, status=404)

    if approval.status == PayoutApproval.Status.EXECUTED:
        # Update txid if the new one is valid and different
        if txid and approval.txid != txid:
            approval.txid = txid
            approval.save(update_fields=['txid', 'updated_at'])
        serializer = PayoutApprovalSerializer(approval)
        return Response(serializer.data)

    mark_executed(approval, txid)

    # Auto-schedule the next cycle if more remain
    if approval.cycle_number < approval.total_cycles:
        from datetime import timedelta
        from django.utils import timezone
        next_due = approval.executed_at + timedelta(minutes=approval.interval_blocks * 10)
        try:
            next_approval, _ = create_pending_approval(
                donation_id=approval.donation_ref,
                donor_email=approval.donor_email,
                donor_name=approval.donor_name,
                recipient_address=approval.recipient_address,
                vault_address=approval.vault_address,
                payout_amount_satoshis=approval.payout_amount_satoshis,
                coin=approval.coin,
                interval_label=approval.interval_label,
                interval_blocks=approval.interval_blocks,
                cycle_number=approval.cycle_number + 1,
                total_cycles=approval.total_cycles,
                due_at=next_due,
            )
            if approval.donation_id and next_approval:
                next_approval.donation_id = approval.donation_id
                next_approval.save(update_fields=['donation'])
        except Exception as exc:
            logger.warning('Failed to create next cycle approval (vault): %s', exc)

    serializer = PayoutApprovalSerializer(approval)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def trigger_approval(request, pk):
    """
    Admin triggers a scheduled withdrawal: refreshes the approval token
    and sends the approval email to the donor.
    Only allowed when the approval is in 'pending' status and due_at has passed.
    """
    try:
        approval = PayoutApproval.objects.get(pk=pk)
    except PayoutApproval.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if approval.status != PayoutApproval.Status.PENDING:
        return Response(
            {'error': f'Cannot trigger: approval is already "{approval.status}"'},
            status=400,
        )

    try:
        refresh_and_send(approval)
    except Exception as exc:
        return Response({'error': f'Email send failed: {exc}'}, status=500)

    serializer = PayoutApprovalSerializer(approval)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_missing_txids(request):
    """
    Diagnostic endpoint: list all executed payouts with missing txids.
    GET /api/payouts/missing-txids/
    """
    missing = PayoutApproval.objects.filter(
        status='executed',
        txid=''
    ).order_by('-executed_at')[:50]
    
    serializer = PayoutApprovalListSerializer(missing, many=True)
    return Response({
        'count': missing.count(),
        'payouts': serializer.data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def notify_reclaim_warning(request):
    """
    Called by the auto-withdraw scheduler when the 2nd withdrawal cycle
    fails. Sends a warning notice to the donor that their funds may
    become reclaimable. No links, no approval — purely informational.
    POST /api/payouts/reclaim-warning/
    """
    data = request.data
    donor_email = (data.get('donor_email') or '').strip()
    if not donor_email:
        return Response({'error': 'donor_email is required'}, status=400)

    try:
        send_reclaim_warning_email(
            donor_email=donor_email,
            donor_name=data.get('donor_name', ''),
            vault_address=data.get('vault_address', ''),
            recipient_address=data.get('recipient_address', ''),
            vault_balance_satoshis=int(data.get('vault_balance_satoshis', 0)),
            coin=data.get('coin', 'BCH'),
            interval_label=data.get('interval_label', ''),
        )
    except Exception as exc:
        logger.warning('Failed to send reclaim warning: %s', exc)
        return Response({'error': f'Email failed: {exc}'}, status=500)

    return Response({'ok': True, 'message': 'Reclaim warning sent'})


# ── Helpers ───────────────────────────────────────────────────────────

def _get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def _approval_html_response(title, message, success=True):
    color = '#4caf50' if success else '#f44336'
    icon = '✓' if success else '✗'
    html = f"""\
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
</head><body style="margin:0;padding:40px 20px;font-family:Arial,sans-serif;
background:#f4f4f4;text-align:center;">
<div style="max-width:480px;margin:0 auto;background:#fff;border-radius:12px;
padding:40px 32px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
<div style="font-size:48px;color:{color};margin-bottom:16px;">{icon}</div>
<h1 style="margin:0 0 12px;font-size:24px;color:#222;">{title}</h1>
<p style="color:#666;font-size:15px;line-height:1.5;">{message}</p>
<p style="margin-top:24px;font-size:12px;color:#aaa;">You can close this tab.</p>
</div></body></html>"""
    return HttpResponse(html, content_type='text/html')
