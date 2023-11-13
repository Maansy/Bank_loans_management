
from .models import Fund, FundRequest, GeneralInfo, FundPayment

class CalculateFundService:
    def __init__(self, fund, amount):
        self.fund = fund
        self.amount = amount

    def call(self):
        return self.amount * self.fund.interest_rate * self.fund.duration / 100
    