from django.contrib import admin
from .models import WalletUser


@admin.register(WalletUser)
class WalletUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'wallet_address', 'display_name', 'last_connected_at', 'created_at']
    search_fields = ['wallet_address', 'display_name']
    readonly_fields = ['created_at', 'updated_at']
