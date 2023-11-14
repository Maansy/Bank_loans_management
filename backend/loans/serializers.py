from .models import Loan, LoanPayment, GeneralInfo, LoanRequest
from rest_framework import serializers
from funds.serializers import FundSerializer
from funds.models import Fund
from users.serializers import LoanCustomerSerializer, BankPersonnelSerializer
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

class LoanRequestSerializer(serializers.ModelSerializer):
    loan = LoanSerializer(read_only=True)
    user = LoanCustomerSerializer(read_only=True)
    assigned_by = BankPersonnelSerializer(read_only=True)
    
    class Meta:
        model = LoanRequest
        fields = '__all__'
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        loan_request = LoanRequest.objects.create(**validated_data)
        return loan_request