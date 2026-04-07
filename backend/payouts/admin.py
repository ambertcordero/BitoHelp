from django.contrib import admin
from .models import PayoutApproval, PayoutAuditLog


class PayoutAuditLogInline(admin.TabularInline):
    model = PayoutAuditLog
    extra = 0
    readonly_fields = ('action', 'detail', 'ip_address', 'user_agent', 'created_at')


@admin.register(PayoutApproval)
class PayoutApprovalAdmin(admin.ModelAdmin):
    list_display = ('id', 'donation_ref', 'cycle_number', 'total_cycles', 'status',
                    'txid', 'donor_email', 'payout_amount_satoshis', 'coin', 'created_at')
    list_filter = ('status', 'coin')
    search_fields = ('donation_ref', 'donor_email', 'recipient_address', 'txid')
    readonly_fields = ('approval_token_hash', 'created_at', 'updated_at')
    inlines = [PayoutAuditLogInline]
