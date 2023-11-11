from .models import Fund
from rest_framework import serializers

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def create(self, validated_data):
        fund = Fund.objects.create(**validated_data)
        return fund