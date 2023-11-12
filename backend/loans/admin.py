from django.contrib import admin
from .models import Loan


class LoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'interest_rate', 'min_loan_amount', 'max_loan_amount', 'duration', 'created_at', 'updated_at', 'created_by')
    search_fields = ('name', 'description', 'interest_rate', 'min_loan_amount', 'max_loan_amount', 'duration', 'created_at', 'updated_at', 'created_by')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Loan,LoanAdmin)