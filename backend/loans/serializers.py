from .models import Loan
from rest_framework import serializers
from funds.serializers import FundSerializer
from funds.models import Fund
class LoanSerializer(serializers.ModelSerializer):
    fund = serializers.PrimaryKeyRelatedField(queryset=Fund.objects.all())
    # fund = FundSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data)
        return loan
    
class LoanSerializer2(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data)
        return loan