from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanCustomerViewSet, LoanProviderViewSet, BankPersonnelViewSet
from .views import CustomLoginView, LogoutView, GetMeView


router = DefaultRouter()
router.register('loan-customer', LoanCustomerViewSet)
router.register('loan-provider', LoanProviderViewSet)
router.register('bank-personnel', BankPersonnelViewSet)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('me/', GetMeView.as_view(), name='get-me'),
    path('logout/', LogoutView.as_view(), name='custom-logout'),
    path('', include(router.urls)),

]
