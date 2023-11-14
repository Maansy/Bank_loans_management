from django.urls import path, register_converter
from .views import create_loan, get_loans, get_loan,calc_interst, request_loan, get_inprogress_loan, get_rejected_loans, approve_loan_request, reject_loan_request
from .converters import FloatConverter
from .views import get_waiting_approve_loans, create_stripe_checkout_session_loan, get_subsribed_loans, get_non_assigned_loan_request

register_converter(FloatConverter, 'float')


urlpatterns = [
    path('create-loan/', create_loan, name='create-loan'),
    path('get-loans/', get_loans, name='get-loans'),
    path('get-loan/<int:pk>/', get_loan, name='get-loan'),
    path('calc-interest/<int:pk>/<float:amount>/', calc_interst, name='calc-interest'),
    path('request-loan/<int:pk>/', request_loan, name='subcribe-loan'),
    path('get-inprogress-loan/', get_inprogress_loan, name='get-approved-loan-waiting-payment'),
    path('get-rejected-loans/', get_rejected_loans, name='get-rejected-loans'),
    path('get-waiting-approve-loans/', get_waiting_approve_loans, name='get-waiting-approve-loans'),
    path('create-checkout-session-loan/', create_stripe_checkout_session_loan, name='create-checkout-session-loan'),
    path('get-subscribed-loans/', get_subsribed_loans, name='get-subscribed-loans'),
    path('get-non-assigned-loan-request/', get_non_assigned_loan_request, name='get-non-assigned-loan-request'),
    path('approve-loan-request/<int:pk>/', approve_loan_request, name='approve-loan-request'),
    path('reject-loan-request/<int:pk>/', reject_loan_request, name='reject-loan-request'),
]