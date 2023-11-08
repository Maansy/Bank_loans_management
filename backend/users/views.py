from rest_framework import viewsets, generics
from .models import LoanCustomer, LoanProvider, BankPersonnel
from .serializers import BankPersonnelSerializer, LoanProviderSerializer, LoanCustomerSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class BankPersonnelViewSet(viewsets.ModelViewSet):
    queryset = BankPersonnel.objects.all()
    serializer_class = BankPersonnelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            bank_personnel = serializer.save()
            return Response({
                'user': UserSerializer(bank_personnel.user).data,
                'message': 'Bank Personnel registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoanProviderViewSet(viewsets.ModelViewSet):
    queryset = LoanProvider.objects.all()
    serializer_class = LoanProviderSerializer

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            loan_customer = serializer.save()
            return Response({
                'user': UserSerializer(loan_customer.user).data,
                'message': 'Loan Customer registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class BankPersonnelRegistrationAPIView(generics.GenericAPIView):
#     serializer_class = BankPersonnelRegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             bank_personnel = serializer.save()
#             return Response({
#                 'user': UserSerializer(bank_personnel.user).data,
#                 'message': 'Bank Personnel registered successfully.'
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoanProviderRegistrationAPIView(generics.GenericAPIView):
#     serializer_class = LoanProviderRegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             loan_provider = serializer.save()
#             return Response({
#                 'user': UserSerializer(loan_provider.user).data,
#                 'message': 'Loan Provider registered successfully.'
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class LoanCustomerRegistrationAPIView(generics.GenericAPIView):
#     serializer_class = LoanCustomerRegistrationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             loan_customer = serializer.save()
#             return Response({
#                 'user': UserSerializer(loan_customer.user).data,
#                 'message': 'Loan Customer registered successfully.'
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class CustomLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Check the type of user and return the appropriate message
            if hasattr(user, 'bank_personnel'):
                return Response({'message': 'You are logged in as Bank Personnel.'}, status=status.HTTP_200_OK)
            elif hasattr(user, 'loan_provider'):
                return Response({'message': 'You are logged in as Loan Provider.'}, status=status.HTTP_200_OK)
            elif hasattr(user, 'loan_customer'):
                return Response({'message': 'You are logged in as Loan Customer.'}, status=status.HTTP_200_OK)
            else:
                # User exists but is not any of the specified types
                return Response({'message': 'You are logged in.'}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
