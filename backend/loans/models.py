from django.db import models

# Create your models here.
class Loan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    interest_rate = models.FloatField()
    max_loan_amount = models.FloatField()
    min_loan_amount = models.FloatField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.BankPersonnel', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name