from .models import Fund, FundRequest , GeneralInfo
from rest_framework import serializers
from users.serializers import LoanProviderSerializer, BankPersonnelSerializer
class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def create(self, validated_data):
        fund = Fund.objects.create(**validated_data)
        return fund
    
class FundRequestSerializer(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)
    user = LoanProviderSerializer(read_only=True)
    assigned_by = BankPersonnelSerializer(read_only=True)
    class Meta:
        model = FundRequest
        fields = '__all__'
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        fund_request = FundRequest.objects.create(**validated_data)
        return fund_request

class GeneralInfoSerializer(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)
    class Meta:
        model = GeneralInfo
        fields = '__all__'
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        general_info = GeneralInfo.objects.create(**validated_data)
        return general_info