from django.db import models

# Create your models here.

class Fund(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    interest_rate = models.FloatField()
    max_fund_amount = models.FloatField()
    min_fund_amount = models.FloatField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.BankPersonnel', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    

class FundRequest(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    user = models.ForeignKey('users.LoanProvider', on_delete=models.CASCADE)
    payed_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    assigned_by = models.ForeignKey('users.BankPersonnel', on_delete=models.CASCADE, null=True, blank=True) 

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.fund.name
    

class GeneralInfo(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    remaining_amount = models.FloatField()
    total_customers = models.IntegerField()
    total_providers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.fund.name
    
class FundPayment(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    user = models.ForeignKey('users.LoanProvider', on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.fund.name