from django.contrib import admin
from .models import Vault, WithdrawalCycle


class WithdrawalCycleInline(admin.TabularInline):
    model = WithdrawalCycle
    extra = 0
    readonly_fields = ('executed_at',)


@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
    list_display = ('donor_display', 'recipient_display', 'status', 'coin',
                    'cycles_completed', 'total_cycles', 'network', 'created_at')
    list_filter = ('status', 'network', 'payout_mode', 'coin')
    search_fields = ('vault_address', 'funder_address', 'recipient_address',
                     'donation_id_ref', 'donor_name', 'recipient_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [WithdrawalCycleInline]
    fieldsets = (
        ('Donor Info', {
            'fields': ('donor_name', 'donor_email', 'funder_address', 'wallet_user'),
        }),
        ('Recipient Info', {
            'fields': ('recipient_name', 'recipient_address', 'cause'),
        }),
        ('Vault Details', {
            'fields': ('donation_id_ref', 'donation', 'vault_address', 'status',
                       'coin', 'network', 'payout_mode', 'contract_params',
                       'withdrawal_satoshis', 'deposit_satoshis', 'interval_blocks',
                       'interval_label', 'funding_txid'),
        }),
        ('Cycle Info', {
            'fields': ('cycles_completed', 'total_cycles', 'last_withdraw_txid',
                       'last_withdraw_at'),
        }),
        ('Reclaim', {
            'fields': ('reclaim_txid', 'reclaimed_at', 'reclaimed_amount',
                       'reclaim_warning_sent_at'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Donor')
    def donor_display(self, obj):
        return obj.donor_name or obj.funder_address[:16] + '…'

    @admin.display(description='Recipient')
    def recipient_display(self, obj):
        return obj.recipient_name or obj.recipient_address[:16] + '…'


@admin.register(WithdrawalCycle)
class WithdrawalCycleAdmin(admin.ModelAdmin):
    list_display = ('vault', 'cycle_donor', 'cycle_recipient', 'cycle_number',
                    'txid', 'amount_satoshis', 'drained', 'executed_at')
    list_filter = ('drained',)
    search_fields = ('txid', 'vault__vault_address', 'vault__donor_name',
                     'vault__recipient_name')

    @admin.display(description='Donor')
    def cycle_donor(self, obj):
        return obj.vault.donor_name or obj.vault.funder_address[:16] + '…'

    @admin.display(description='Recipient')
    def cycle_recipient(self, obj):
        return obj.vault.recipient_name or obj.vault.recipient_address[:16] + '…'
