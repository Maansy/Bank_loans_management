from django.urls import path, include
from .views import create_fund, get_funds

urlpatterns = [
    path('create-fund/', create_fund, name='create-fund'),
    path('get-funds/', get_funds, name='get-funds'),
]