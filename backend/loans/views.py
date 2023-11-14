from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Loan, LoanRequest, GeneralInfo, LoanPayment
from .serializers import LoanSerializer, LoanSerializer2, LoanRequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from funds.models import Fund
from .services import LoanCalculator
import stripe


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_loan(request):
    if request.method == 'POST':
        user = request.user
        try:
            bank_personnal = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=bank_personnal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_loans(request):
    if request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer2(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_loan(request,pk):
    if request.method == 'GET':
        try:
            loan = Loan.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def calc_interst(request, pk, amount):
    if request.method == 'GET':
        try:
            loan = Loan.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        loan_calculator = LoanCalculator(amount, loan.duration, loan.interest_rate, loan.interest_type)
        interest = loan_calculator.calculate_interest()
        monthly_payment = loan_calculator.calculate_monthly_payment()
        return Response({'interest': interest, 'monthly_payment':monthly_payment}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def request_loan(request,pk):
    if request.method == 'POST':
        user = request.user
        try:
            loan_customer = user.loan_customer
        except:
            return Response({'error': 'You are not a loan customer'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            loan = Loan.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LoanRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=loan_customer, loan=loan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_rejected_loans(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_customer = user.loan_customer
        except:
            return Response({'error': 'You are not a loan customer'}, status=status.HTTP_400_BAD_REQUEST)
        fund_requests = LoanRequest.objects.filter(is_rejected=True, is_payed=False, user=loan_customer)
        serializer = LoanRequestSerializer(fund_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_waiting_approve_loans(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_customer = user.loan_customer
        except:
            return Response({'error': 'You are not a loan customer'}, status=status.HTTP_400_BAD_REQUEST)
        loan_requests = LoanRequest.objects.filter(is_approved=False, is_rejected=False, is_payed=False, user=loan_customer)
        serializer = LoanRequestSerializer(loan_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_inprogress_loan(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_customer = user.loan_customer
        except:
            return Response({'error': 'You are not a loan customer'}, status=status.HTTP_400_BAD_REQUEST)
        loan_requests = LoanRequest.objects.filter(is_approved=True, is_payed=False, user=loan_customer)
        print(loan_requests)
        data = []
        for loan_request in loan_requests:
            loan = loan_request.loan
            loan_calculator = LoanCalculator(loan_request.payed_amount, loan.duration, loan.interest_rate, loan.interest_type)
            monthly_payment = loan_calculator.calculate_monthly_payment()
            data.append({'id':loan_request.id,'duration': loan.duration * 12, 'payed_amount': loan_request.payed_amount,'loan': loan.name, 'monthly_payment': round(monthly_payment,2)})
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_subsribed_loans(request):
    if request.method == 'GET':
        user = request.user
        try:
            loan_customer = user.loan_customer
        except:
            return Response({'error': 'You are not a loan customer'}, status=status.HTTP_400_BAD_REQUEST)
        loan_requests = LoanRequest.objects.filter(is_approved=True, is_payed=True, user=loan_customer)
        print(loan_requests)
        data = []
        for loan_request in loan_requests:
            loan = loan_request.loan
            loan_calculator = LoanCalculator(loan_request.payed_amount, loan.duration, loan.interest_rate, loan.interest_type)
            monthly_payment = loan_calculator.calculate_monthly_payment()
            data.append({'id':loan_request.id,'duration': loan.duration * 12, 'payed_amount': loan_request.payed_amount,'loan': loan.name, 'monthly_payment': round(monthly_payment,2)})
        return Response(data, status=status.HTTP_200_OK)

stripe.api_key = 'sk_test_51O6FfiCPlb6OgBYTGZfUHyHesnm1Y1TFAF3vbPyLw8zotPtAoZATwmuG4iSsuAp7NHZJWBlFkTSwjzcXkMptPqof00hXweSPZn'
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_stripe_checkout_session_loan(request):
    try:
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
            success_url=request.build_absolute_uri('http://localhost:8080/customer-dashboard'),  # Redirect URLs after successful payment            
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        # we should create a webhook to change the is_payed to true
        loan_id = request.data['id']
        loan_request = LoanRequest.objects.get(pk=loan_id)
        loan_request.is_payed = True
        loan_request.save()
        loan_payment = LoanPayment.objects.create(loan=loan_request.loan, user=loan_request.user, amount=request.data['amount'])
        loan_payment.save()

        return Response({'sessionId': checkout_session.id})
    except Exception as e:
        print(e)
        return Response({'error': str(e)}, status=400)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_non_assigned_loan_request(request):
    if request.method == 'GET':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        loan_requests = LoanRequest.objects.filter(is_approved=False, is_rejected = False, is_payed=False, assigned_by=None)
        serializer = LoanRequestSerializer(loan_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def approve_loan_request(request, pk):
    if request.method == 'PUT':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            loan_request = LoanRequest.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan request not found'}, status=status.HTTP_404_NOT_FOUND)
        loan_request.is_approved = True
        loan_request.assigned_by = bank_personnel
        loan_request.save()
        return Response({'message': 'Loan request approved successfully'}, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def reject_loan_request(request, pk):
    if request.method == 'PUT':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            loan_request = LoanRequest.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan request not found'}, status=status.HTTP_404_NOT_FOUND)
        loan_request.is_rejected = True
        loan_request.assigned_by = bank_personnel
        loan_request.save()
        return Response({'message': 'Loan request rejected successfully'}, status=status.HTTP_200_OK)