from .models import Loan
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def create(self, validated_data):
        loan = Loan.objects.create(**validated_data)
        return loan