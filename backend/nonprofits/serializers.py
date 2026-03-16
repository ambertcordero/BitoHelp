from rest_framework import serializers
from .models import Nonprofit

class NonprofitSerializer(serializers.ModelSerializer):
    """Full nonprofit serializer with all fields"""
    class Meta:
        model = Nonprofit
        fields = [
            'id',
            'name',
            'description',
            'bch_address',
            'website',
            'email',
            'phone',
            'category',
            'logo_url',
            'verified',
            'active',
            'created_at',
            'updated_at',
            'total_donations',
            'donation_count'
        ]
        read_only_fields = [
            'id', 
            'created_at', 
            'updated_at',
            'total_donations', 
            'donation_count'
        ]

class NonprofitListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for dropdown/list views"""
    class Meta:
        model = Nonprofit
        fields = ['id', 'name', 'bch_address', 'category', 'verified']
