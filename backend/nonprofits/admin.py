from django.contrib import admin
from .models import Nonprofit

@admin.register(Nonprofit)
class NonprofitAdmin(admin.ModelAdmin):
    list_display = ('name', 'bch_address', 'category', 'verified', 'active', 'donation_count', 'total_donations', 'created_at')
    list_filter = ('category', 'verified', 'active')
    search_fields = ('name', 'description', 'bch_address')
    ordering = ('-verified', 'name')
    readonly_fields = ('created_at', 'updated_at', 'total_donations', 'donation_count')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'logo_url'),
        }),
        ('Wallet Address', {
            'fields': ('bch_address',),
            'description': 'The BCH wallet address for this organization. Must be unique.',
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone'),
        }),
        ('Status', {
            'fields': ('verified', 'active'),
        }),
        ('Statistics (read-only)', {
            'fields': ('total_donations', 'donation_count', 'created_at', 'updated_at'),
        }),
    )
