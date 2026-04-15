from rest_framework import serializers
from .models import PayoutApproval, PayoutAuditLog


class PayoutApprovalSerializer(serializers.ModelSerializer):
    payout_id = serializers.IntegerField(source='id', read_only=True)
    transaction_id = serializers.CharField(source='txid', read_only=True)
    donation_txid = serializers.CharField(source='donation.txid', default='', read_only=True)

    class Meta:
        model = PayoutApproval
        fields = [
            'id', 'payout_id', 'transaction_id', 'donation_txid', 'donation_ref', 'donor_email', 'donor_name',
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
    payout_id = serializers.IntegerField(source='id', read_only=True)
    transaction_id = serializers.CharField(source='txid', read_only=True)
    donation_txid = serializers.CharField(source='donation.txid', default='', read_only=True)
    payout_mode = serializers.CharField(source='donation.payout_mode', default='smart', read_only=True)
    donation_id = serializers.IntegerField(source='donation.id', default=None, read_only=True)

    class Meta:
        model = PayoutApproval
        fields = [
            'id', 'payout_id', 'transaction_id', 'donation_txid', 'donation_ref', 'donation_id', 'cycle_number', 'total_cycles',
            'payout_amount_satoshis', 'coin', 'status',
            'due_at', 'interval_label', 'interval_blocks',
            'donor_email', 'donor_name',
            'recipient_address', 'vault_address',
            'payout_mode',
            'approval_expires_at', 'approved_at', 'executed_at',
            'txid', 'created_at',
        ]
        read_only_fields = fields


class PayoutAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutAuditLog
        fields = ['id', 'action', 'detail', 'ip_address', 'created_at']
        read_only_fields = fields
