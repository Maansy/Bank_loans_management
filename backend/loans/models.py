from django.db import models
from funds.models import Fund
# Create your models here.
class Loan(models.Model):
    
    LOAN_TYPE_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    
    INTEREST_TYPE_CHOICES = (
        ('fixed', 'Fixed'),
        ('reducing', 'Reducing'),
    )

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    interest_rate = models.FloatField()
    max_loan_amount = models.FloatField()
    min_loan_amount = models.FloatField()
    duration = models.IntegerField()
    loan_type = models.CharField(max_length=100, choices=LOAN_TYPE_CHOICES, null=True, blank=True)
    interest_type = models.CharField(max_length=100, choices=INTEREST_TYPE_CHOICES, null=True, blank=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.BankPersonnel', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
class LoanRequest(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    user = models.ForeignKey('users.LoanCustomer', on_delete=models.CASCADE)
    payed_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    assigned_by = models.ForeignKey('users.BankPersonnel', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.loan.name
    

class GeneralInfo(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    user = models.ForeignKey('users.LoanCustomer', on_delete=models.CASCADE)
    total_amount = models.FloatField()
    remaining_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.loan.name

class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    user = models.ForeignKey('users.LoanCustomer', on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.loan.name