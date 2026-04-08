from rest_framework import serializers
from .models import WalletUser


class WalletUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletUser
        fields = ['id', 'wallet_address', 'display_name', 'avatar_url',
                  'last_connected_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'last_connected_at', 'created_at', 'updated_at']


class WalletConnectSerializer(serializers.Serializer):
    wallet_address = serializers.CharField(max_length=255)
