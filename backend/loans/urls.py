from django.urls import path, include
from .views import create_loan, get_loans

urlpatterns = [
    path('create-loan/', create_loan, name='create-loan'),
    path('get-loans/', get_loans, name='get-loans'),
]