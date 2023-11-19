from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import BankPersonnel, LoanCustomer, LoanProvider
    

class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.fund_data = {'name': 'testfund', 'description': 'testdescription', 'interest_rate': 10.0, 'max_fund_amount': 100000.0, 'min_fund_amount':1000.0 , 'duration': 12}
        
        self.user_bank = User.objects.create(username='testuser', password='testpassword')
        self.bank_personnel = BankPersonnel.objects.create(user=self.user_bank, bank_name='testbank', bank_branch='testbranch', contact_number='1234567890', address='testaddress', city='testcity', state='teststate')
        
        self.user_provider = User.objects.create(username='testuser2', password='testpassword')
        self.loan_provider = LoanProvider.objects.create(user=self.user_provider, contact_number='1234567890', address='testaddress', city='testcity', state='teststate' , max_amount=100000.0)
        
        self.user_customer = User.objects.create(username='testuser3', password='testpassword')
        self.loan_customer = LoanCustomer.objects.create(user=self.user_customer, contact_number='1234567890', address='testaddress', city='testcity', state='teststate' , max_income=100000.0)

        self.fund_request = {'payed_amount': 1000.0}
    
    # here we make some functions to authenticate the user and post/get data

    def authenticate_and_post_fund(self,user):
        self.client.force_authenticate(user=user)
        return self.client.post(reverse('create-fund'), self.fund_data)
    
    def authenticate_and_get_funds(self,user):
        self.client.force_authenticate(user=user)
        return self.client.get(reverse('get-funds'))
    
    def authenticate_and_get_fund(self,user, fund_id):
        self.client.force_authenticate(user=user)
        return self.client.get(reverse('get-fund', args=[fund_id]))
    
    def authenticate_and_request_fund(self,user, fund_id):
        self.client.force_authenticate(user=user)
        return self.client.post(reverse('request-fund', args=[fund_id]), self.fund_request)
    
    def authenticate_and_approve_fund_request(self,user, fund_id):
        self.client.force_authenticate(user=user)
        return self.client.put(reverse('approve-fund-request', args=[fund_id]))
    
    def authenticate_and_reject_fund_request(self,user, fund_id):
        self.client.force_authenticate(user=user)
        return self.client.put(reverse('reject-fund-request', args=[fund_id]))
    
    def authenticate_and_get_non_assigned_fund_request(self,user):
        self.client.force_authenticate(user=user)
        return self.client.get(reverse('get-fund-request'))
    
    # here we will test that only a banker can create a fund

    def test_banker_can_create_fund(self):
        response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_provider_cannot_create_fund(self):
        response = self.authenticate_and_post_fund(self.user_provider)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_create_fund(self):
        response = self.authenticate_and_post_fund(self.user_customer)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    # here we will test that only a banker or provider can get funds

    def test_banker_can_get_funds(self):
        self.authenticate_and_post_fund(self.user_bank)
        response = self.authenticate_and_get_funds(self.user_bank)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_provider_can_get_funds(self):
        self.authenticate_and_post_fund(self.user_bank)
        response = self.authenticate_and_get_funds(self.user_provider)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_customer_cannot_get_funds(self):
        self.authenticate_and_post_fund(self.user_bank)
        response = self.authenticate_and_get_funds(self.user_customer)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    # here we will test that only a banker or provider can get a fund

    def test_banker_can_get_fund(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        response = self.authenticate_and_get_fund(self.user_bank, fund_id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_provider_can_get_fund(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        response = self.authenticate_and_get_fund(self.user_provider, fund_id)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_get_fund(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        response = self.authenticate_and_get_fund(self.user_customer, fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    # here we will test that only a provider can request a fund
    
    def test_provider_can_request_fund(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        response = self.authenticate_and_request_fund(self.user_provider, fund_id)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_customer_cannot_request_fund(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        response = self.authenticate_and_request_fund(self.user_customer, fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_banker_cannot_request_fund(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        response = self.authenticate_and_request_fund(self.user_bank, fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    # here we will test that only a banker can approve a fund request

    def test_banker_can_approve_fund_request(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        request_fund_response = self.authenticate_and_request_fund(self.user_provider, fund_id)
        self.assertEquals(request_fund_response.status_code, status.HTTP_201_CREATED)
        
        request_fund_id = request_fund_response.data.get('id')
        response = self.authenticate_and_approve_fund_request(self.user_bank, request_fund_id)

        self.assertEquals(response.status_code, status.HTTP_200_OK)  

    def test_provider_cannot_approve_fund_request(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        request_fund_response = self.authenticate_and_request_fund(self.user_provider, fund_id)
        self.assertEquals(request_fund_response.status_code, status.HTTP_201_CREATED)

        request_fund_id = request_fund_response.data.get('id')
        response = self.authenticate_and_approve_fund_request(self.user_provider, request_fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)      

    def test_customer_cannot_approve_fund_request(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        request_fund_response = self.authenticate_and_request_fund(self.user_provider, fund_id)
        self.assertEquals(request_fund_response.status_code, status.HTTP_201_CREATED)

        request_fund_id = request_fund_response.data.get('id')
        response = self.authenticate_and_approve_fund_request(self.user_customer, request_fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    # here we will test that only a banker can reject a fund request

    def test_banker_can_reject_fund_request(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)

        fund_id = post_response.data['id']
        request_fund_response = self.authenticate_and_request_fund(self.user_provider, fund_id)
        self.assertEquals(request_fund_response.status_code, status.HTTP_201_CREATED)

        request_fund_id = request_fund_response.data.get('id')
        response = self.authenticate_and_reject_fund_request(self.user_bank, request_fund_id)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
    
    def test_provider_cannot_reject_fund_request(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)
        
        fund_id = post_response.data['id']
        request_fund_response = self.authenticate_and_request_fund(self.user_provider, fund_id)
        self.assertEquals(request_fund_response.status_code, status.HTTP_201_CREATED)

        request_fund_id = request_fund_response.data.get('id')
        response = self.authenticate_and_reject_fund_request(self.user_provider, request_fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_customer_cannot_reject_fund_request(self):
        post_response = self.authenticate_and_post_fund(self.user_bank)
        self.assertEquals(post_response.status_code, status.HTTP_201_CREATED)
        
        fund_id = post_response.data['id']
        request_fund_response = self.authenticate_and_request_fund(self.user_provider, fund_id)
        self.assertEquals(request_fund_response.status_code, status.HTTP_201_CREATED)

        request_fund_id = request_fund_response.data.get('id')
        response = self.authenticate_and_reject_fund_request(self.user_customer, request_fund_id)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # here we will test that only a banker can get non assigned fund requests

    def test_banker_can_get_non_assigned_fund_request(self):
        response = self.authenticate_and_get_non_assigned_fund_request(self.user_bank)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_provider_cannot_get_non_assigned_fund_request(self):
        response = self.authenticate_and_get_non_assigned_fund_request(self.user_provider)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_cannot_get_non_assigned_fund_request(self):
        response = self.authenticate_and_get_non_assigned_fund_request(self.user_customer)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)