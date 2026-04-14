from rest_framework import serializers
from .models import WalletUser


class WalletUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletUser
        fields = ['id', 'wallet_address', 'display_name', 'email', 'contact',
                  'avatar_url', 'last_connected_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'last_connected_at', 'created_at', 'updated_at']


class WalletConnectSerializer(serializers.Serializer):
    wallet_address = serializers.CharField(max_length=255)
    display_name = serializers.CharField(max_length=255, required=False, allow_blank=True, default='')
    email = serializers.EmailField(required=False, allow_blank=True, default='')
    contact = serializers.CharField(max_length=50, required=False, allow_blank=True, default='')
