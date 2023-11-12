from django.urls import path, include
from .views import create_loan, get_loans, get_loan

urlpatterns = [
    path('create-loan/', create_loan, name='create-loan'),
    path('get-loans/', get_loans, name='get-loans'),
    path('get-loan/<int:pk>/', get_loan, name='get-loan'),
]