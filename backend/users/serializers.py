from rest_framework import serializers
from .models import BankPersonnel, LoanProvider, LoanCustomer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BankPersonnelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BankPersonnel
        fields = '__all__'
        extra_kwargs = {
            'is_active': {'default': True, 'read_only': True},
            'is_verified': {'default': False, 'read_only': True},
            'is_deleted': {'default': False, 'read_only': True},
            'min_value': {'default': 0},
            'max_value': {'default': 0},
            'min_duration': {'default': 0},
            'max_duration': {'default': 0},
            'min_interest': {'default': 0},
            'max_interest': {'default': 0},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        bank_personnel = BankPersonnel.objects.create(
            user=user, **validated_data)
        return bank_personnel


class LoanProviderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LoanProvider
        fields = '__all__'

        extra_kwargs = {
            'is_active': {'default': True, 'read_only': True},
            'is_verified': {'default': False, 'read_only': True},
            'is_deleted': {'default': False, 'read_only': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        loan_provider = LoanProvider.objects.create(
            user=user, **validated_data)
        return loan_provider


class LoanCustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LoanCustomer
        fields = '__all__'

        extra_kwargs = {
            'is_active': {'default': True, 'read_only': True},
            'is_verified': {'default': False, 'read_only': True},
            'is_deleted': {'default': False, 'read_only': True},
        }

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        loan_customer = LoanCustomer.objects.create(
            user=user, **validated_data)
        return loan_customer

# class BankPersonnelRegistrationSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = BankPersonnel
#         fields = '__all__'

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = UserSerializer.create(UserSerializer(), validated_data=user_data)
#         bank_personnel = BankPersonnel.objects.create(user=user, **validated_data)
#         return bank_personnel


# class LoanProviderRegistrationSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = LoanProvider
#         fields = '__all__'

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = UserSerializer.create(UserSerializer(), validated_data=user_data)
#         loan_provider = LoanProvider.objects.create(user=user, **validated_data)
#         return loan_provider

# class LoanCustomerRegistrationSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = LoanCustomer
#         fields = '__all__'

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = UserSerializer.create(UserSerializer(), validated_data=user_data)
#         loan_customer = LoanCustomer.objects.create(user=user, **validated_data)
#         return loan_customer
