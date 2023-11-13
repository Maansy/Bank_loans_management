class LoanCalculator:
    def __init__(self, principal, duration, interest_rate, interest_type):
        self.principal = principal
        self.duration = duration
        self.interest_rate = interest_rate
        self.interest_type = interest_type

    def calculate_interest(self):
        """Calculate interest based on the type of the loan."""
        if self.interest_type == 'fixed':
            return self.calc_fixed_interest()
        elif self.interest_type == 'reducing':
            return self.calc_reducing_interest()
        else:
            raise ValueError("Invalid loan type")
        
    def calc_fixed_interest(self):
        """Calculate total interest for a fixed interest rate loan."""
        return self.principal * self.interest_rate * self.duration / 100
    
    def calc_reducing_interest(self):
        """Calculate total interest for a reducing balance loan."""
        total_interest = 0
        remaining_principal = self.principal
        for _ in range(self.duration):
            interest_for_the_year = remaining_principal * self.interest_rate / 100
            total_interest += interest_for_the_year
            remaining_principal -= self.principal / self.duration
        return total_interest
    
    def calculate_monthly_payment(self):
        """Calculate monthly payment for a loan."""
        return (self.principal + self.calculate_interest()) / (self.duration * 12)