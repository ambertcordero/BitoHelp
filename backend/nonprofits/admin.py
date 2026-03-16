from django.contrib import admin
from .models import Nonprofit

@admin.register(Nonprofit)
class NonprofitAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'verified', 'active', 'donation_count', 'total_donations', 'created_at')
    list_filter = ('category', 'verified', 'active')
    search_fields = ('name', 'description', 'bch_address')
    ordering = ('-verified', 'name')
    readonly_fields = ('created_at', 'updated_at', 'total_donations', 'donation_count')
