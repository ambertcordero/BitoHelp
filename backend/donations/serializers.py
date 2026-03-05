from rest_framework import serializers
from .models import Donation


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ['timestamp']


class DonationStatsSerializer(serializers.Serializer):
    total_donations = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=16, decimal_places=8)
    total_by_cause = serializers.DictField()
    total_by_coin = serializers.DictField()
