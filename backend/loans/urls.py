from django.urls import path, register_converter
from .views import create_loan, get_loans, get_loan,calc_interst
from .converters import FloatConverter


register_converter(FloatConverter, 'float')


urlpatterns = [
    path('create-loan/', create_loan, name='create-loan'),
    path('get-loans/', get_loans, name='get-loans'),
    path('get-loan/<int:pk>/', get_loan, name='get-loan'),
    path('calc-interest/<int:pk>/<float:amount>/', calc_interst, name='calc-interest'),
]