from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'coin', 'cause', 'recipient', 'timestamp', 'reclaim_txid']
    list_filter = ['coin', 'cause', 'timestamp']
    search_fields = ['donor_name', 'donor_email', 'txid', 'recipient', 'cause']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Transaction Info', {
            'fields': ('txid', 'reclaim_txid', 'explorer_url', 'timestamp')
        }),
        ('Donation Details', {
            'fields': ('recipient', 'amount', 'coin', 'cause', 'message')
        }),
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_contact')
        }),
    )
