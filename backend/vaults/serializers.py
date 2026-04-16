from rest_framework import serializers
from .models import Vault, WithdrawalCycle


class WithdrawalCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalCycle
        fields = ['id', 'cycle_number', 'txid', 'amount_satoshis', 'drained', 'executed_at']
        read_only_fields = ['id', 'executed_at']


class VaultListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = [
            'id', 'donation_id_ref', 'vault_address', 'recipient_address',
            'recipient_name', 'funder_address', 'withdrawal_satoshis', 'deposit_satoshis',
            'interval_blocks', 'interval_label', 'contract_params',
            'payout_mode', 'coin', 'network', 'status',
            'cycles_completed', 'total_cycles',
            'donor_email', 'donor_name', 'cause',
            'funding_txid', 'last_withdraw_txid', 'last_withdraw_at',
            'reclaim_txid', 'reclaimed_at', 'reclaimed_amount',
            'reclaim_warning_sent_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VaultDetailSerializer(VaultListSerializer):
    withdrawal_cycles = WithdrawalCycleSerializer(many=True, read_only=True)

    class Meta(VaultListSerializer.Meta):
        fields = VaultListSerializer.Meta.fields + ['withdrawal_cycles']


class VaultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = [
            'donation_id_ref', 'vault_address', 'recipient_address',
            'recipient_name', 'funder_address', 'withdrawal_satoshis', 'deposit_satoshis',
            'interval_blocks', 'interval_label', 'contract_params',
            'payout_mode', 'coin', 'network', 'status',
            'total_cycles', 'donor_email', 'donor_name', 'cause',
            'funding_txid',
        ]


class VaultUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = [
            'status', 'cycles_completed', 'last_withdraw_txid', 'last_withdraw_at',
            'reclaim_txid', 'reclaimed_at', 'reclaimed_amount',
            'reclaim_warning_sent_at',
        ]
