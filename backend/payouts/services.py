"""
Payout Approval service layer.

Responsibilities:
- Create pending approval records with secure hashed tokens
- Build and send Gmail-compatible action emails (Schema.org ConfirmAction)
- Process Gmail callback: validate token, execute payout, send confirmation
"""

import logging
import os
from datetime import timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.utils import timezone
from django.utils.html import strip_tags
from email.mime.image import MIMEImage

from .models import PayoutApproval, PayoutAuditLog

logger = logging.getLogger(__name__)

PHT = ZoneInfo('Asia/Manila')


# ── Create a pending approval ──────────────────────────────────────────

def create_pending_approval(
    *,
    donation_id,
    donor_email,
    donor_name='',
    recipient_address,
    vault_address='',
    payout_amount_satoshis,
    coin='BCH',
    interval_label='',
    interval_blocks=1,
    cycle_number=1,
    total_cycles=1,
    vault_balance_satoshis=None,
    due_at=None,
    idempotency_key=None,
):
    """
    Create a PayoutApproval record and return (approval, raw_token).
    The raw_token is included in the email link; only its hash is stored.

    If an approval with the same idempotency_key exists, returns it
    (with raw_token=None since the original token is not recoverable).
    """
    if due_at is None:
        due_at = timezone.now()

    if idempotency_key is None:
        idempotency_key = f'{donation_id}:cycle:{cycle_number}'

    raw_token, hashed_token = PayoutApproval.generate_token()

    try:
        approval = PayoutApproval.objects.create(
            donation_ref=donation_id,
            donor_email=donor_email,
            donor_name=donor_name,
            recipient_address=recipient_address,
            vault_address=vault_address,
            payout_amount_satoshis=payout_amount_satoshis,
            coin=coin,
            interval_label=interval_label,
            interval_blocks=interval_blocks,
            cycle_number=cycle_number,
            total_cycles=total_cycles,
            due_at=due_at,
            approval_token_hash=hashed_token,
            approval_expires_at=timezone.now() + timedelta(hours=24),
            idempotency_key=idempotency_key,
        )
    except IntegrityError:
        # Duplicate idempotency_key — check if existing is expired/failed
        existing = PayoutApproval.objects.filter(idempotency_key=idempotency_key).first()
        if existing:
            if existing.status in (PayoutApproval.Status.EXPIRED, PayoutApproval.Status.FAILED):
                # Replace stale approval: delete old, create fresh one
                existing.delete()
                approval = PayoutApproval.objects.create(
                    donation_ref=donation_id,
                    donor_email=donor_email,
                    donor_name=donor_name,
                    recipient_address=recipient_address,
                    vault_address=vault_address,
                    payout_amount_satoshis=payout_amount_satoshis,
                    coin=coin,
                    interval_label=interval_label,
                    interval_blocks=interval_blocks,
                    cycle_number=cycle_number,
                    total_cycles=total_cycles,
                    due_at=due_at,
                    approval_token_hash=hashed_token,
                    approval_expires_at=timezone.now() + timedelta(hours=24),
                    idempotency_key=idempotency_key,
                )
                PayoutAuditLog.objects.create(
                    payout_approval=approval,
                    action=PayoutAuditLog.Action.CREATED,
                    detail=f'Replaced expired/failed approval for {payout_amount_satoshis} sats',
                )
                approval._vault_balance_satoshis = vault_balance_satoshis
                return approval, raw_token
            return existing, None
        raise

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.CREATED,
        detail=f'Pending approval created for {payout_amount_satoshis} sats to {recipient_address}',
    )

    # Stash vault balance on the instance so send_approval_email can use it
    approval._vault_balance_satoshis = vault_balance_satoshis
    return approval, raw_token


# ── Send approval email ────────────────────────────────────────────────

def send_approval_email(approval, raw_token):
    """
    Send an email with Gmail ConfirmAction (Schema.org) JSON-LD so the donor
    can approve the payout with a single tap inside Gmail.
    """
    base_url = getattr(settings, 'SITE_BASE_URL', 'http://localhost:8001')
    action_url = f'{base_url}/api/payouts/approve/{raw_token}/'

    sats = approval.payout_amount_satoshis
    bch_amount = f'{sats / 1e8:.8f}'

    subject = f'[CrypToCare] Approve payout of {bch_amount} {approval.coin} (cycle {approval.cycle_number}/{approval.total_cycles})'

    # Gmail ConfirmAction JSON-LD
    json_ld = {
        '@context': 'http://schema.org',
        '@type': 'EmailMessage',
        'potentialAction': {
            '@type': 'ConfirmAction',
            'name': f'Approve {bch_amount} {approval.coin} payout',
            'handler': {
                '@type': 'HttpActionHandler',
                'url': action_url,
                'method': 'HttpRequestMethod/POST',
            },
        },
        'description': (
            f'Approve withdrawal of {bch_amount} {approval.coin} '
            f'to {approval.recipient_address} (cycle {approval.cycle_number}/{approval.total_cycles})'
        ),
    }

    vault_balance_sats = getattr(approval, '_vault_balance_satoshis', None)
    html_body = _build_fallback_html(approval, bch_amount, action_url, json_ld, vault_balance_sats=vault_balance_sats)
    text_body = strip_tags(html_body)

    sender = getattr(settings, 'PAYOUT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=sender,
        to=[approval.donor_email],
    )
    msg.attach_alternative(html_body, 'text/html')

    # Attach logo as CID inline image
    logo_path = os.path.join(settings.BASE_DIR, '..', 'src', 'logo.png')
    if os.path.isfile(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
        logo_img = MIMEImage(logo_data, _subtype='png')
        logo_img.add_header('Content-ID', '<cryptocare_logo>')
        logo_img.add_header('Content-Disposition', 'inline', filename='logo.png')
        msg.attach(logo_img)

    msg.send(fail_silently=False)

    approval.email_sent_at = timezone.now()
    approval.save(update_fields=['email_sent_at'])

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.EMAIL_SENT,
        detail=f'Approval email sent to {approval.donor_email}',
    )

    logger.info('Approval email sent for %s cycle %d', approval.donation_ref, approval.cycle_number)


def _build_fallback_html(approval, bch_amount, action_url, json_ld, vault_balance_sats=None):
    """Inline HTML email with CrypToCare branding, PHT timezone, and cycle format."""
    import json
    ld_script = json.dumps(json_ld, indent=2)
    truncated_addr = (
        f'{approval.recipient_address[:10]}...{approval.recipient_address[-6:]}'
        if len(approval.recipient_address) > 20
        else approval.recipient_address
    )
    expires_pht = approval.approval_expires_at.astimezone(PHT)
    expires_str = expires_pht.strftime('%b %d, %Y %I:%M %p') + ' PHT'
    cycle_str = f'{approval.cycle_number}/{approval.total_cycles}'
    vault_balance_bch = f'{vault_balance_sats / 1e8:.8f}' if vault_balance_sats is not None else None

    return f"""\
<html><head>
<script type="application/ld+json">{ld_script}</script>
</head><body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:30px 0;">
<tr><td align="center">
<table width="520" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

<!-- Logo Header -->
<tr><td align="center" style="padding:28px 24px 12px;">
  <img src="cid:cryptocare_logo" alt="CrypToCare" width="180" style="max-width:180px;height:auto;" />
</td></tr>

<!-- Title -->
<tr><td align="center" style="padding:4px 24px 6px;">
  <h2 style="margin:0;font-size:22px;color:#222;">Payout Approval Required</h2>
</td></tr>
<tr><td align="center" style="padding:0 24px 20px;">
  <p style="margin:0;font-size:15px;color:#666;">A scheduled withdrawal is ready for your donation.</p>
</td></tr>

<!-- Details Table -->
<tr><td style="padding:0 32px;">
  <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
    <tr>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#888;width:110px;">Amount</td>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#222;font-weight:600;">{bch_amount} {approval.coin}</td>
    </tr>
    <tr>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#888;">Recipient</td>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#222;font-weight:600;">{truncated_addr}</td>
    </tr>
    <tr>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#888;">Cycle</td>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#222;font-weight:600;">{cycle_str}</td>
    </tr>
    {'<tr><td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#888;">Vault Balance</td><td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#222;font-weight:600;">' + vault_balance_bch + ' ' + approval.coin + '</td></tr>' if vault_balance_bch else ''}
    <tr>
      <td style="padding:12px 0;font-size:14px;color:#888;">Expires</td>
      <td style="padding:12px 0;font-size:14px;color:#222;font-weight:600;">{expires_str}</td>
    </tr>
  </table>
</td></tr>

<!-- Approve Button -->
<tr><td align="center" style="padding:28px 24px 12px;">
  <a href="{action_url}" style="display:inline-block;padding:14px 40px;background:#4caf50;color:#ffffff;text-decoration:none;border-radius:6px;font-weight:bold;font-size:16px;letter-spacing:0.3px;">Approve Payout</a>
</td></tr>

<!-- Fallback link -->
<tr><td align="center" style="padding:4px 24px 24px;">
  <p style="margin:0;font-size:12px;color:#aaa;">If the button doesn&#39;t work, copy this link into your browser:<br/>
  <a href="{action_url}" style="color:#4caf50;word-break:break-all;">{action_url}</a></p>
</td></tr>

<!-- Footer -->
<tr><td style="background:#fafafa;padding:16px 24px;border-top:1px solid #eee;">
  <p style="margin:0;font-size:11px;color:#999;text-align:center;">
    This approval link expires in 24 hours. Do not share it with anyone.<br/>
    &copy; CrypToCare &mdash; Empowering transparent giving on Bitcoin Cash.
  </p>
</td></tr>

</table>
</td></tr>
</table>
</body></html>"""


# ── Process Gmail action callback ──────────────────────────────────────

def process_approval(raw_token, ip_address='', user_agent=''):
    """
    Validate the token, mark as approved, and return the approval record.
    Does NOT execute the payout (that's a separate step to avoid blocking
    the Gmail action callback response).
    """
    hashed = PayoutApproval.hash_token(raw_token)
    approval = PayoutApproval.objects.filter(approval_token_hash=hashed).first()

    if not approval:
        PayoutAuditLog.objects.create(
            payout_approval_id=0,  # orphan — no matching record
            action=PayoutAuditLog.Action.APPROVAL_ATTEMPT,
            detail='Invalid token',
            ip_address=ip_address,
            user_agent=user_agent[:500],
        ) if False else None  # skip orphan log (no FK target)
        return None, 'Invalid or unknown approval token.'

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.APPROVAL_ATTEMPT,
        detail=f'Approval attempt from {ip_address}',
        ip_address=ip_address,
        user_agent=user_agent[:500],
    )

    if approval.status != PayoutApproval.Status.PENDING:
        return approval, f'This payout has already been {approval.status}.'

    if approval.is_expired:
        approval.status = PayoutApproval.Status.EXPIRED
        approval.save(update_fields=['status', 'updated_at'])
        PayoutAuditLog.objects.create(
            payout_approval=approval,
            action=PayoutAuditLog.Action.EXPIRED,
            detail='Token expired at approval attempt',
        )
        return approval, 'This approval link has expired.'

    # Mark approved
    approval.status = PayoutApproval.Status.APPROVED
    approval.approved_at = timezone.now()
    approval.save(update_fields=['status', 'approved_at', 'updated_at'])

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.APPROVED,
        detail='Approved via email action',
        ip_address=ip_address,
        user_agent=user_agent[:500],
    )

    logger.info('Payout approved: %s cycle %d', approval.donation_ref, approval.cycle_number)
    return approval, None


def mark_executed(approval, txid):
    """Called after the frontend or a background task successfully withdraws."""
    approval.status = PayoutApproval.Status.EXECUTED
    approval.executed_at = timezone.now()
    approval.txid = txid
    approval.save(update_fields=['status', 'executed_at', 'txid', 'updated_at'])

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.EXECUTED,
        detail=f'Payout executed: txid={txid}',
    )


def mark_failed(approval, error_message):
    """Called if withdrawal execution fails."""
    approval.status = PayoutApproval.Status.FAILED
    approval.execution_error = error_message
    approval.save(update_fields=['status', 'execution_error', 'updated_at'])

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.EXECUTION_FAILED,
        detail=error_message[:1000],
    )


def refresh_and_send(approval):
    """
    Generate a fresh approval token, extend the expiry window, and
    re-send the approval email.  Used when the nonprofit admin clicks
    "Withdraw Now" from the dashboard.
    """
    import hashlib
    import secrets as _secrets

    raw_token = _secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    approval.approval_token_hash = hashed_token
    approval.approval_expires_at = timezone.now() + timedelta(hours=24)
    approval.save(update_fields=['approval_token_hash', 'approval_expires_at', 'updated_at'])

    PayoutAuditLog.objects.create(
        payout_approval=approval,
        action=PayoutAuditLog.Action.CREATED,
        detail='Approval token refreshed and email re-sent by admin.',
    )

    send_approval_email(approval, raw_token)


# ── Reclaim warning email ────────────────────────────────────────────

def send_reclaim_warning_email(
    *,
    donor_email,
    donor_name='',
    vault_address='',
    recipient_address='',
    vault_balance_satoshis=0,
    coin='BCH',
    interval_label='',
):
    """
    Send a plain notice email to the donor warning them that a recipient has
    failed to withdraw for the 2nd consecutive interval. If the 3rd cycle
    also goes unwithdrawn, the donor will be able to reclaim the funds.
    No links, no action buttons — purely informational.
    """
    bch_balance = f'{vault_balance_satoshis / 1e8:.8f}' if vault_balance_satoshis else '0.00000000'
    truncated_vault = (
        f'{vault_address[:12]}...{vault_address[-6:]}'
        if len(vault_address) > 22
        else vault_address
    )
    truncated_recipient = (
        f'{recipient_address[:12]}...{recipient_address[-6:]}'
        if len(recipient_address) > 22
        else recipient_address
    )

    subject = '[CrypToCare] Withdrawal warning \u2014 recipient has not withdrawn for 2 intervals'
    greeting = f'Hi {donor_name},' if donor_name else 'Hi,'
    interval_note = f' ({interval_label} each)' if interval_label else ''

    html_body = f"""\
<html><head></head>
<body style="margin:0;padding:0;background:#f4f4f4;font-family:Arial,Helvetica,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f4;padding:30px 0;">
<tr><td align="center">
<table width="520" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

<!-- Logo Header -->
<tr><td align="center" style="padding:28px 24px 12px;">
  <img src="cid:cryptocare_logo" alt="CrypToCare" width="180" style="max-width:180px;height:auto;" />
</td></tr>

<!-- Title -->
<tr><td align="center" style="padding:4px 24px 6px;">
  <h2 style="margin:0;font-size:22px;color:#e65100;">Withdrawal Warning</h2>
</td></tr>
<tr><td style="padding:0 32px 20px;">
  <p style="margin:0;font-size:15px;color:#666;line-height:1.6;">
    {greeting}<br/><br/>
    The recipient of one of your donations has <strong>failed to withdraw for
    2 consecutive intervals</strong>{interval_note}.
    <br/><br/>
    If the recipient does not withdraw during the <strong>3rd interval</strong>,
    the remaining funds in the vault will become <strong>eligible for you to reclaim</strong>
    back to your wallet through the Donor Dashboard's <strong>Reclaim</strong> tab.
  </p>
</td></tr>

<!-- Details Table -->
<tr><td style="padding:0 32px;">
  <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
    <tr>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#888;width:130px;">Vault Balance</td>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#e65100;font-weight:700;">{bch_balance} {coin}</td>
    </tr>
    <tr>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#888;">Vault Address</td>
      <td style="padding:12px 0;border-bottom:1px solid #eee;font-size:14px;color:#222;font-weight:600;">{truncated_vault}</td>
    </tr>
    <tr>
      <td style="padding:12px 0;font-size:14px;color:#888;">Recipient</td>
      <td style="padding:12px 0;font-size:14px;color:#222;font-weight:600;">{truncated_recipient}</td>
    </tr>
  </table>
</td></tr>

<!-- Footer -->
<tr><td style="background:#fafafa;padding:16px 24px;border-top:1px solid #eee;">
  <p style="margin:0;font-size:11px;color:#999;text-align:center;">
    This is an automated notice. No action is required at this time.<br/>
    &copy; CrypToCare &mdash; Empowering transparent giving on Bitcoin Cash.
  </p>
</td></tr>

</table>
</td></tr>
</table>
</body></html>"""

    text_body = strip_tags(html_body)

    sender = getattr(settings, 'PAYOUT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=sender,
        to=[donor_email],
    )
    msg.attach_alternative(html_body, 'text/html')

    # Attach logo as CID inline image
    logo_path = os.path.join(settings.BASE_DIR, '..', 'src', 'logo.png')
    if os.path.isfile(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
        logo_img = MIMEImage(logo_data, _subtype='png')
        logo_img.add_header('Content-ID', '<cryptocare_logo>')
        logo_img.add_header('Content-Disposition', 'inline', filename='logo.png')
        msg.attach(logo_img)

    msg.send(fail_silently=False)
    logger.info('Reclaim warning email sent to %s for vault %s', donor_email, vault_address)
