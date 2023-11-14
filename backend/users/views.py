from rest_framework import viewsets, generics
from .models import LoanCustomer, LoanProvider, BankPersonnel
from .serializers import BankPersonnelSerializer, LoanProviderSerializer, LoanCustomerSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.utils.http import http_date


class BankPersonnelViewSet(viewsets.ModelViewSet):
    queryset = BankPersonnel.objects.all()
    serializer_class = BankPersonnelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == 'post' or self.action == 'create':
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bank_personnel = serializer.save()
            user = bank_personnel.user
            return Response({
                'user': UserSerializer(bank_personnel.user).data,
                'message': 'Bank Personnel registered successfully.',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanProviderViewSet(viewsets.ModelViewSet):
    queryset = LoanProvider.objects.all()
    serializer_class = LoanProviderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == 'post' or self.action == 'create':
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            loan_provider = serializer.save()
            return Response({
                'user': UserSerializer(loan_provider.user).data,
                'message': 'Loan Provider registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanCustomerViewSet(viewsets.ModelViewSet):
    queryset = LoanCustomer.objects.all()
    serializer_class = LoanCustomerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == 'post' or self.action == 'create':
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            loan_customer = serializer.save()
            return Response({
                'user': UserSerializer(loan_customer.user).data,
                'message': 'Loan Customer registered successfully.',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user': UserSerializer(user).data,
                'message': 'You are logged in.',
                'token': token.key,
            }
            if hasattr(user, 'bank_personnel'):
                data['role'] = 'bank'
                data['is_verified'] = user.bank_personnel.is_verified
            elif hasattr(user, 'loan_provider'):
                data['role'] = 'provider'
                data['is_verified'] = user.loan_provider.is_verified
            elif hasattr(user, 'loan_customer'):
                data['role'] = 'customer'
                data['is_verified'] = user.loan_customer.is_verified

            response = Response(data, status=status.HTTP_200_OK)

   
            expiry = getattr(settings, 'TOKEN_EXPIRY', 3600)
            max_age = expiry if expiry is not None else 365 * \
                24 * 60 * 60  # One year if expiry is None

            secure = getattr(settings, 'SESSION_COOKIE_SECURE', False)
            httponly = getattr(settings, 'SESSION_COOKIE_HTTPONLY', True)
            samesite = getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Lax')

            response.set_cookie(
                'auth_token',
                token.key,
                max_age=max_age,
                expires=http_date(datetime.utcnow().timestamp() + max_age),
                secure=secure,
                httponly=httponly,
                samesite=samesite
            )
            response.set_cookie(
                'role',
                data['role'],
                max_age=max_age,
                expires=http_date(datetime.utcnow().timestamp() + max_age),
                secure=secure,
                httponly=httponly,
                samesite=samesite
            )

            return response
        else:
            # Authentication failed
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        response = Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK)

        response.delete_cookie('auth_token')

        return response


class GetMeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        if hasattr(request.user, 'bank_personnel'):
            user_data['role'] = 'bank'
            bank_personnel_data = BankPersonnelSerializer(
                request.user.bank_personnel).data
            user_data.update(bank_personnel_data)
        elif hasattr(request.user, 'loan_provider'):
            user_data['role'] = 'provider'
            loan_provider_data = LoanProviderSerializer(
                request.user.loan_provider).data
            user_data.update(loan_provider_data)
        elif hasattr(request.user, 'loan_customer'):
            user_data['role'] = 'customer'
            loan_customer_data = LoanCustomerSerializer(
                request.user.loan_customer).data
            user_data.update(loan_customer_data)
        else:
            user_data['role'] = 'user'

        return Response(user_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_non_verified_providers(request):
    if request.method == 'GET':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        loan_providers = LoanProvider.objects.filter(is_verified=False)
        serializer = LoanProviderSerializer(loan_providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_non_verified_customers(request):
    if request.method == 'GET':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        customers = LoanCustomer.objects.filter(is_verified=False)
        serializer = LoanCustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def verify_provider(request,pk):
    if request.method == 'PUT':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            loan_provider = LoanProvider.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan provider not found'}, status=status.HTTP_404_NOT_FOUND)
        loan_provider.is_verified = True
        loan_provider.save()
        serializer = LoanProviderSerializer(loan_provider)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def verify_customer(request,pk):
    if request.method == 'PUT':
        user = request.user
        try:
            bank_personnel = user.bank_personnel
        except:
            return Response({'error': 'You are not a bank personnel'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = LoanCustomer.objects.get(pk=pk)
        except:
            return Response({'error': 'Loan provider not found'}, status=status.HTTP_404_NOT_FOUND)
        customer.is_verified = True
        customer.save()
        serializer = LoanCustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
