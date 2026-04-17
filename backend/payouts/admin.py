from django.contrib import admin
from django.utils.html import format_html
from .models import PayoutApproval, PayoutAuditLog


class PayoutAuditLogInline(admin.TabularInline):
    model = PayoutAuditLog
    extra = 0
    readonly_fields = ('action', 'detail', 'ip_address', 'user_agent', 'created_at')


@admin.register(PayoutApproval)
class PayoutApprovalAdmin(admin.ModelAdmin):
    list_display = (
        'vault_id_display', 'id', 'cycle_display', 'status_badge',
        'amount_display', 'coin', 'interval_label',
        'txid_short', 'donor_email', 'created_at',
    )
    list_display_links = ('id',)
    list_filter = ('status', 'coin', 'vault_id')
    search_fields = ('vault_id', 'donation_ref', 'donor_email', 'recipient_address', 'txid')
    readonly_fields = ('vault_id', 'approval_token_hash', 'created_at', 'updated_at')
    ordering = ('vault_id', 'cycle_number')
    list_per_page = 50
    inlines = [PayoutAuditLogInline]

    @admin.display(description='Vault', ordering='vault_id')
    def vault_id_display(self, obj):
        return format_html(
            '<span style="background:#fff3cd; color:#856404; padding:2px 8px; '
            'border-radius:6px; font-weight:700; font-size:12px;">{}</span>',
            obj.vault_id or '\u2014'
        )

    @admin.display(description='Cycle', ordering='cycle_number')
    def cycle_display(self, obj):
        return f'{obj.cycle_number} / {obj.total_cycles}'

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            'pending': ('#fff3cd', '#856404'),
            'approved': ('#d1ecf1', '#0c5460'),
            'executed': ('#d4edda', '#155724'),
            'expired': ('#f8d7da', '#721c24'),
            'failed': ('#f8d7da', '#721c24'),
        }
        bg, fg = colors.get(obj.status, ('#e2e3e5', '#383d41'))
        return format_html(
            '<span style="background:{}; color:{}; padding:2px 8px; '
            'border-radius:4px; font-weight:600; font-size:11px; text-transform:uppercase;">{}</span>',
            bg, fg, obj.get_status_display()
        )

    @admin.display(description='Amount (sats)', ordering='payout_amount_satoshis')
    def amount_display(self, obj):
        bch = obj.payout_amount_satoshis / 1e8
        sats_fmt = f'{obj.payout_amount_satoshis:,.0f}'
        bch_fmt = f'{bch:.8f}'
        return format_html(
            '{} <span style="color:#999; font-size:11px;">({}BCH)</span>',
            sats_fmt, bch_fmt
        )

    @admin.display(description='TXID', ordering='txid')
    def txid_short(self, obj):
        if not obj.txid:
            return '\u2014'
        return format_html(
            '<span style="font-family:monospace; font-size:11px;" title="{}">{}&hellip;</span>',
            obj.txid, obj.txid[:16]
        )
