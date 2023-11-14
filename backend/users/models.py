from django.db import models
from django.contrib.auth.models import User

class BankPersonnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_personnel')
    bank_name = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.user.username

class LoanProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loan_provider')
    max_amount = models.FloatField(default=0)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.user.username

class LoanCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loan_customer')
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_income = models.FloatField(default=0)
    
    
    def __str__(self):
        return self.user.username
