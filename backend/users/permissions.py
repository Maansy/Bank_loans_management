from rest_framework.permissions import BasePermission

class IsBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'bank_personnel')

class IsLoanProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'loan_provider')
    
class IsLoanCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and hasattr(request.user, 'loan_customer')
    
class IsBankPersonnelOrLoanProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (hasattr(request.user, 'bank_personnel') or hasattr(request.user, 'loan_provider'))
    
class IsBankPersonnelOrLoanCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (hasattr(request.user, 'bank_personnel') or hasattr(request.user, 'loan_customer'))
    
