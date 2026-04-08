import hashlib
import secrets
from django.db import models
from django.utils import timezone
from datetime import timedelta


def default_expiry():
    return timezone.now() + timedelta(hours=24)


class PayoutApproval(models.Model):
    """
    Tracks a pending (or completed) payout that requires donor approval
    via Gmail one-click action before funds are released.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        EXECUTED = 'executed', 'Executed'
        EXPIRED = 'expired', 'Expired'
        FAILED = 'failed', 'Failed'

    # Donation / schedule reference
    donation_ref = models.CharField(max_length=128, db_index=True,
                                    help_text='Frontend-generated donation ID string')
    donation = models.ForeignKey(
        'donations.Donation', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='payout_approvals',
    )

    # Donor info
    donor_email = models.EmailField(blank=True)
    donor_name = models.CharField(max_length=255, blank=True)

    # Payout details
    recipient_address = models.CharField(max_length=255)
    txid = models.CharField(max_length=255, blank=True)
    vault_address = models.CharField(max_length=255, blank=True)
    payout_amount_satoshis = models.BigIntegerField()
    coin = models.CharField(max_length=20, default='BCH')
    interval_label = models.CharField(max_length=50, blank=True)
    interval_blocks = models.PositiveIntegerField(default=1)
    cycle_number = models.PositiveIntegerField(default=1)
    total_cycles = models.PositiveIntegerField(default=1)

    # Scheduling
    due_at = models.DateTimeField()

    # Security: store only hashed token
    approval_token_hash = models.CharField(max_length=128, unique=True)
    approval_expires_at = models.DateTimeField(default=default_expiry)

    # Timestamps for state transitions
    email_sent_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    # Execution result
    txid = models.CharField(max_length=255, blank=True)
    execution_error = models.TextField(blank=True)

    # Status
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True,
    )

    # Idempotency key — prevents duplicate approval records for same cycle
    idempotency_key = models.CharField(max_length=255, unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Payout Approval'
        verbose_name_plural = 'Payout Approvals'
        indexes = [
            models.Index(fields=['donation_ref', 'status']),
            models.Index(fields=['approval_token_hash']),
        ]

    def __str__(self):
        return f"PayoutApproval {self.donation_ref} cycle {self.cycle_number} [{self.status}]"

    @property
    def is_expired(self):
        return timezone.now() > self.approval_expires_at

    @property
    def is_actionable(self):
        return self.status == self.Status.PENDING and not self.is_expired

    # ── Token helpers ──

    @staticmethod
    def generate_token():
        """Return (raw_token, hashed_token) pair."""
        raw = secrets.token_urlsafe(48)
        hashed = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        return raw, hashed

    @staticmethod
    def hash_token(raw_token):
        return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()


class PayoutAuditLog(models.Model):
    class Action(models.TextChoices):
        CREATED = 'created', 'Created'
        EMAIL_SENT = 'email_sent', 'Email Sent'
        APPROVAL_ATTEMPT = 'approval_attempt', 'Approval Attempt'
        APPROVED = 'approved', 'Approved'
        EXECUTION_START = 'execution_start', 'Execution Start'
        EXECUTED = 'executed', 'Executed'
        EXECUTION_FAILED = 'execution_failed', 'Execution Failed'
        EXPIRED = 'expired', 'Expired'
        REJECTED = 'rejected', 'Rejected'

    payout_approval = models.ForeignKey(
        PayoutApproval, on_delete=models.CASCADE, related_name='audit_logs',
    )
    action = models.CharField(max_length=30, choices=Action.choices)
    detail = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.action} @ {self.created_at:%Y-%m-%d %H:%M}"
