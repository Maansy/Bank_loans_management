from django.contrib import admin
from .models import Fund, FundRequest , GeneralInfo, FundPayment

class FundAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'interest_rate', 'min_fund_amount', 'max_fund_amount', 'duration', 'created_at', 'updated_at', 'created_by')
    search_fields = ('name', 'description', 'interest_rate', 'min_fund_amount', 'max_fund_amount', 'duration', 'created_at', 'updated_at', 'created_by')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class FundRequestAdmin(admin.ModelAdmin):
    list_display = ('fund', 'user', 'payed_amount', 'created_at', 'is_approved', 'is_rejected')
    search_fields = ('fund', 'user', 'payed_amount', 'created_at', 'is_approved')
    readonly_fields = ('created_at', 'is_approved')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class GeneralInfoAdmin(admin.ModelAdmin):
    list_display = ('fund', 'total_amount', 'remaining_amount', 'total_customers', 'total_providers', 'created_at', 'updated_at')
    search_fields = ('fund', 'total_amount', 'remaining_amount', 'total_customers', 'total_providers', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class FundPaymentAdmin(admin.ModelAdmin):
    list_display = ('fund', 'user', 'amount', 'created_at')
    search_fields = ('fund', 'user', 'amount', 'created_at')
    readonly_fields = ('created_at',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Fund,FundAdmin)
admin.site.register(FundRequest,FundRequestAdmin)
admin.site.register(GeneralInfo,GeneralInfoAdmin)
admin.site.register(FundPayment,FundPaymentAdmin)