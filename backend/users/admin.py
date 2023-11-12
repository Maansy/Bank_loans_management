from django.contrib import admin
from .models import BankPersonnel, LoanProvider, LoanCustomer
# Register your models here.

class BankPersonnelAdmin(admin.ModelAdmin):

    list_display = ('get_username', 'is_verified', 'is_active', 'created_at', 'updated_at')
    search_fields = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(BankPersonnel,BankPersonnelAdmin)

class LoanProviderAdmin(admin.ModelAdmin):
    # we need to get user.username to add here
    list_display = ('get_username', 'is_verified', 'is_active', 'created_at', 'updated_at')
    search_fields = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username' 

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(LoanProvider,LoanProviderAdmin)

class LoanCustomerAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'is_verified', 'is_active', 'created_at', 'updated_at')
    search_fields = ('is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(LoanCustomer,LoanCustomerAdmin)
