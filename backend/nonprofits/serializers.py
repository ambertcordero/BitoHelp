from rest_framework import serializers
from .models import Nonprofit

class NonprofitSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Nonprofit
        fields = ['id', 'name', 'bch_address', 'category', 'verified']


class ReceivedDonationSerializer(serializers.ModelSerializer):
    """Lightweight serializer for donations received by a nonprofit."""
    class Meta:
        from donations.models import Donation
        model = Donation
        fields = [
            'id', 'txid', 'amount', 'coin', 'cause', 'message',
            'donor_name', 'donor_email', 'timestamp', 'interval',
            'wallet_address', 'explorer_url',
        ]


class NonprofitProfileSerializer(serializers.ModelSerializer):
    donations = serializers.SerializerMethodField()
    unique_donor_count = serializers.SerializerMethodField()
    total_received_bch = serializers.SerializerMethodField()

    class Meta:
        model = Nonprofit
        fields = [
            'id', 'name', 'description', 'bch_address', 'website',
            'email', 'phone', 'category', 'logo_url', 'verified',
            'active', 'created_at', 'updated_at', 'total_donations',
            'donation_count', 'donations', 'unique_donor_count',
            'total_received_bch',
        ]

    def get_donations(self, obj):
        from donations.models import Donation
        qs = Donation.objects.filter(nonprofit=obj).order_by('-timestamp')
        return ReceivedDonationSerializer(qs, many=True).data

    def get_unique_donor_count(self, obj):
        from donations.models import Donation
        return (
            Donation.objects.filter(nonprofit=obj)
            .exclude(wallet_address='')
            .values('wallet_address')
            .distinct()
            .count()
        )

    def get_total_received_bch(self, obj):
        from donations.models import Donation
        from django.db.models import Sum
        total = Donation.objects.filter(nonprofit=obj).aggregate(s=Sum('amount'))['s']
        return str(total or 0)
