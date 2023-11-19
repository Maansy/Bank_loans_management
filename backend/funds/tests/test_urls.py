from django.test import SimpleTestCase
from django.urls import reverse, resolve
from funds.views import create_fund, get_funds,get_fund,request_fund,approve_fund_request,get_non_assigned_fund_request, reject_fund_request,get_approved_fund_request
from funds.views import get_rejected_fund_request, calc_fund_interest, get_approved_fund_waiting_payment, get_rejected_funds,get_waiting_approve_funds, get_payed_funds_with_interests,create_stripe_checkout_session

#reverse: it will return the url for the given name
#resolve: it will return the name of the url for the given url
# we use SimpleTestCase because we are not using any database
# we use reverse and resolve to check if the url is resolved correctly
class TestUrls(SimpleTestCase):
    
    def test_create_fund_url_is_resolved(self):
        url = reverse('create-fund')
        self.assertEquals(resolve(url).func, create_fund)

    def test_get_funds_url_is_resolved(self):
        url = reverse('get-funds')
        self.assertEquals(resolve(url).func, get_funds)

    def test_get_fund_url_is_resolved(self):
        url = reverse('get-fund' , args=[1])
        self.assertEquals(resolve(url).func, get_fund)
        
    def test_request_fund_url_is_resolved(self):
        url = reverse('request-fund' , args=[1])
        self.assertEquals(resolve(url).func, request_fund)

    def test_approve_fund_request_url_is_resolved(self):
        url = reverse('approve-fund-request' , args=[1])
        self.assertEquals(resolve(url).func, approve_fund_request)

    def test_get_non_assigned_fund_request_url_is_resolved(self):
        url = reverse('get-fund-request')
        self.assertEquals(resolve(url).func, get_non_assigned_fund_request)

    def test_reject_fund_request_url_is_resolved(self):
        url = reverse('reject-fund-request' , args=[1])
        self.assertEquals(resolve(url).func, reject_fund_request)
    
    def test_get_approved_fund_request_url_is_resolved(self):
        url = reverse('get-approved-fund-request')
        self.assertEquals(resolve(url).func, get_approved_fund_request)

    def test_get_rejected_fund_request_url_is_resolved(self):
        url = reverse('get-rejected-fund-request')
        self.assertEquals(resolve(url).func, get_rejected_fund_request)

    def test_calc_fund_interest_url_is_resolved(self):
        url = reverse('calc-fund-interest' , args=[1,100.0])
        self.assertEquals(resolve(url).func, calc_fund_interest)

    def test_get_approved_fund_waiting_payment_url_is_resolved(self):
        url = reverse('get-approved-fund-waiting-payment')
        self.assertEquals(resolve(url).func, get_approved_fund_waiting_payment)
    
    def test_get_waiting_approve_funds_url_is_resolved(self):
        url = reverse('get-waiting-approve-funds')
        self.assertEquals(resolve(url).func, get_waiting_approve_funds)
    
    def test_get_rejected_funds_url_is_resolved(self):
        url = reverse('get-rejected-funds')
        self.assertEquals(resolve(url).func, get_rejected_funds)

    def test_get_payed_funds_with_interests_url_is_resolved(self):
        url = reverse('get-payed-funds-with-interests')
        self.assertEquals(resolve(url).func, get_payed_funds_with_interests)

    def test_create_stripe_checkout_session_url_is_resolved(self):
        url = reverse('create-stripe-checkout-session')
        self.assertEquals(resolve(url).func, create_stripe_checkout_session)
