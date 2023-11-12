from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_loans(request):
    if request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
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