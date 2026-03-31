from rest_framework import serializers
from .models import PayoutApproval, PayoutAuditLog


class PayoutApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutApproval
        fields = [
            'id', 'donation_ref', 'donor_email', 'donor_name',
            'recipient_address', 'vault_address',
            'payout_amount_satoshis', 'coin',
            'interval_label', 'interval_blocks',
            'cycle_number', 'total_cycles', 'due_at',
            'approval_expires_at', 'email_sent_at',
            'approved_at', 'executed_at', 'txid',
            'execution_error', 'status', 'idempotency_key',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields


class PayoutApprovalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutApproval
        fields = [
            'id', 'donation_ref', 'cycle_number', 'total_cycles',
            'payout_amount_satoshis', 'coin', 'status',
            'approval_expires_at', 'approved_at', 'executed_at',
            'txid', 'created_at',
        ]
        read_only_fields = fields


class PayoutAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutAuditLog
        fields = ['id', 'action', 'detail', 'ip_address', 'created_at']
        read_only_fields = fields
