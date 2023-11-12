from django.urls import path, include
from .views import create_fund, get_funds,get_fund

urlpatterns = [
    path('create-fund/', create_fund, name='create-fund'),
    path('get-funds/', get_funds, name='get-funds'),
    path('get-fund/<int:pk>/', get_fund, name='get-fund'),
]