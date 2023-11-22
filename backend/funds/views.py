from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Fund, FundRequest, GeneralInfo, FundPayment
from .serializers import FundSerializer, FundRequestSerializer, GeneralInfoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .services import CalculateFundService
import stripe
from users.permissions import IsBankPersonnel, IsLoanProvider, IsLoanCustomer, IsBankPersonnelOrLoanProvider, IsBankPersonnelOrLoanCustomer
from django.conf import settings

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnel])
def create_fund(request):
    if request.method == 'POST':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=bank_personnal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnelOrLoanProvider])
def get_funds(request):
    if request.method == 'GET':
        funds = Fund.objects.all()
        serializer = FundSerializer(funds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnelOrLoanProvider])
def get_fund(request,pk):
    if request.method == 'GET':
        try:
            fund = Fund.objects.get(pk=pk)
        except:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FundSerializer(fund)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsLoanProvider])
def request_fund(request,pk):
    if request.method == 'POST':
        user = request.user
        try:
            loan_provider = user.loan_provider
        except:
            return Response({'error': 'You are not a loan provider'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            fund = Fund.objects.get(pk=pk)
        except:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FundRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=loan_provider, fund=fund)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnel])
def approve_fund_request(request,pk):
    if request.method == 'PUT':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            fund_request = FundRequest.objects.get(pk=pk)
        except:
            return Response({'error': 'Fund request not found'}, status=status.HTTP_404_NOT_FOUND)
        fund_request.is_approved = True
        fund_request.assigned_by = bank_personnal
        fund_request.save()
        serializer = FundRequestSerializer(fund_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnel])
def reject_fund_request(request,pk):
    if request.method == 'PUT':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            fund_request = FundRequest.objects.get(pk=pk)
        except:
            return Response({'error': 'Fund request not found'}, status=status.HTTP_404_NOT_FOUND)
        fund_request.is_rejected = True
        fund_request.assigned_by = bank_personnal
        fund_request.save()
        serializer = FundRequestSerializer(fund_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnel])
def get_non_assigned_fund_request(request):
    if request.method == 'GET':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_approved=False, is_rejected=False, assigned_by=None)
        serializer = FundRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnel])
def get_approved_fund_request(request):
    if request.method == 'GET':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_approved=True, is_rejected=False)
        serializer = FundRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnel])
def get_rejected_fund_request(request):
    if request.method == 'GET':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_approved=False, is_rejected=True)
        serializer = FundRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsBankPersonnelOrLoanProvider])
def calc_fund_interest(request,pk,amount):
    if request.method == 'GET':
        try:
            fund = Fund.objects.get(pk=pk)
        except:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
        calc_fund = CalculateFundService(fund, amount)
        total_amount = calc_fund.call() + amount
        return Response(total_amount, status=status.HTTP_200_OK)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsLoanProvider])
def get_approved_fund_waiting_payment(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_provider = user.loan_provider
        except:
            return Response({'error': 'You are not a loan provider'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_approved=True, is_payed=False, user=loan_provider)
        serializer = FundRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsLoanProvider])
def get_rejected_funds(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_provider = user.loan_provider
        except:
            return Response({'error': 'You are not a loan provider'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_rejected=True, is_payed=False, user=loan_provider)
        serializer = FundRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsLoanProvider])
def get_waiting_approve_funds(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_provider = user.loan_provider
        except:
            return Response({'error': 'You are not a loan provider'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_approved=False, is_rejected=False, is_payed=False, user=loan_provider)
        serializer = FundRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsLoanProvider])
def get_payed_funds_with_interests(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_provider = user.loan_provider
        except:
            return Response({'error': 'You are not a loan provider'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = FundRequest.objects.filter(is_payed=True, user=loan_provider)
        data = []
        for fund_request in fund_requests:
            calc_fund = CalculateFundService(fund_request.fund, fund_request.payed_amount)
            total_amount = calc_fund.call() + fund_request.payed_amount
            data.append({'fund_name': fund_request.fund.name, 'total_amount': total_amount, 'payed_amount': fund_request.payed_amount})
        return Response(data, status=status.HTTP_200_OK)
    
# import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_stripe_checkout_session(request):
    try:
        print(request.data)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Fund Subscription',
                        },
                        'unit_amount': int(float(request.data['amount'] * 100)) ,  # Convert to cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('http://localhost:8080/provider-dashboard'),  # Redirect URLs after successful payment            
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        #we should create a webhook to change the is_payed to true
        fund_id = request.data['id']
        fund_request = FundRequest.objects.get(pk=fund_id)
        fund_request.is_payed = True
        fund_request.save()
        try:
            general_info = GeneralInfo.objects.get(fund=fund_request.fund)
            general_info.total_amount += fund_request.payed_amount
            general_info.remaining_amount += fund_request.payed_amount
            general_info.total_providers += 1
            general_info.save()
        except:
            GeneralInfo.objects.create(fund=fund_request.fund, total_amount=fund_request.payed_amount, remaining_amount=fund_request.payed_amount, total_providers=1, total_customers=0)

        fund_payment = FundPayment.objects.create(fund=fund_request.fund, user=fund_request.user, amount=fund_request.payed_amount)
        fund_payment.save()

        return Response({'sessionId': checkout_session.id})
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=400)

