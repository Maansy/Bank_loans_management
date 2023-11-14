from django.contrib import admin
from .models import Loan, LoanRequest, GeneralInfo, LoanPayment


class LoanAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'interest_rate', 'min_loan_amount', 'max_loan_amount', 'duration', 'created_at', 'updated_at', 'created_by')
    search_fields = ('name', 'description', 'interest_rate', 'min_loan_amount', 'max_loan_amount', 'duration', 'created_at', 'updated_at', 'created_by')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Loan,LoanAdmin)


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('loan', 'user', 'payed_amount', 'created_at', 'is_approved', 'is_rejected', 'is_payed', 'assigned_by')
    search_fields = ('loan', 'user', 'payed_amount', 'created_at', 'is_approved', 'is_rejected', 'is_payed', 'assigned_by')
    readonly_fields = ('created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(LoanRequest,LoanRequestAdmin)


class GeneralInfoAdmin(admin.ModelAdmin):
    list_display = ('loan', 'user', 'total_amount', 'remaining_amount', 'created_at', 'updated_at')
    search_fields = ('loan', 'user', 'total_amount', 'remaining_amount', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(GeneralInfo,GeneralInfoAdmin)

class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'user', 'amount', 'created_at')
    search_fields = ('loan', 'user', 'amount', 'created_at')
    readonly_fields = ('created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(LoanPayment,LoanPaymentAdmin)