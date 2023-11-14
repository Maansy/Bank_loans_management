from django.urls import path, include
from .views import create_fund, get_funds,get_fund,request_fund,approve_fund_request,get_non_assigned_fund_request, reject_fund_request,get_approved_fund_request
from .views import get_rejected_fund_request, calc_fund_interest, get_approved_fund_waiting_payment, get_rejected_funds,get_waiting_approve_funds, get_payed_funds_with_interests,create_stripe_checkout_session

urlpatterns = [
    path('create-fund/', create_fund, name='create-fund'),
    path('get-funds/', get_funds, name='get-funds'),
    path('get-fund/<int:pk>/', get_fund, name='get-fund'),
    path('request-fund/<int:pk>/', request_fund, name='request-fund'),
    path('approve-fund-request/<int:pk>/', approve_fund_request, name='approve-fund-request'),
    path('get-non-assigned-fund-request/', get_non_assigned_fund_request, name='get-fund-request'),
    path('reject-fund-request/<int:pk>/', reject_fund_request, name='reject-fund-request'),
    path('get-approved-fund-request/', get_approved_fund_request, name='get-approved-fund-request'),
    path('get-rejected-fund-request/', get_rejected_fund_request, name='get-rejected-fund-request'),
    path('calc-fund-interest/<int:pk>/<float:amount>/', calc_fund_interest, name='calc-fund-interest'),
    path('get-approved-fund-waiting-payment/', get_approved_fund_waiting_payment, name='get-approved-fund-waiting-payment'),
    path('get-waiting-approve-funds/', get_waiting_approve_funds, name='get-waiting-approve-funds'),
    path('get-rejected-funds/', get_rejected_funds, name='get-rejected-funds'),
    path('get-payed-funds-with-interests/', get_payed_funds_with_interests, name='get-payed-funds-with-interests'),
    path('create-stripe-checkout-session/', create_stripe_checkout_session, name='create-stripe-checkout-session'),
]