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