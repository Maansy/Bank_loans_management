from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BankPersonnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_personnel')
    bank_name = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.user.username

class LoanProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='loan_provider')
    company_name = models.CharField(max_length=100)
    company_branch = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
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
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=0)
    min_duration = models.IntegerField(default=0)
    max_duration = models.IntegerField(default=0)
    min_interest = models.FloatField(default=0)
    max_interest = models.FloatField(default=0)
    
    
    def __str__(self):
        return self.user.username
