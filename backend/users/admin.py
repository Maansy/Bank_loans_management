from django.contrib import admin
from .models import BankPersonnel, LoanProvider, LoanCustomer
# Register your models here.

admin.site.register(BankPersonnel)
admin.site.register(LoanProvider)
admin.site.register(LoanCustomer)
