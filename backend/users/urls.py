from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanCustomerViewSet, LoanProviderViewSet, BankPersonnelViewSet
from .views import CustomLoginView, LogoutView, GetMeView, get_non_verified_providers,get_non_verified_customers, verify_customer, verify_provider


router = DefaultRouter()
router.register('loan-customer', LoanCustomerViewSet)
router.register('loan-provider', LoanProviderViewSet)
router.register('bank-personnel', BankPersonnelViewSet)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('me/', GetMeView.as_view(), name='get-me'),
    path('logout/', LogoutView.as_view(), name='custom-logout'),
    path('', include(router.urls)),
    path('get-non-verified-providers/', get_non_verified_providers, name='get-non-verified-providers'),
    path('get-non-verified-customers/', get_non_verified_customers, name='get-non-verified-customers'),
    path('verify-customer/<int:pk>/', verify_customer, name='verify-customer'),
    path('verify-provider/<int:pk>/', verify_provider, name='verify-provider'),
]
