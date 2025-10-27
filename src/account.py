import re

class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.express_transfer_fee = 1

        if len(pesel) != 11:
            self.pesel = "Invalid"
        else:
            self.pesel = pesel

        gets_bonus = self.check_year_of_birth(self.pesel) 

        pattern = r"^PROM_.+"

        if promo_code and re.fullmatch(pattern, promo_code) and gets_bonus:
            self.balance += 50

    def check_year_of_birth(self, pesel):
        if pesel == "Invalid":
            return False
        
        month = int(pesel[2:4])

        if month >= 21 and month <= 32:
            year_of_birth = 2000 + int(pesel[:2])
        elif month >= 41 and month <= 52:
            year_of_birth = 2100 + int(pesel[:2])
        elif month >= 61 and month <= 72:
            year_of_birth = 2200 + int(pesel[:2])
        else:
            year_of_birth = 1900 + int(pesel[:2])

        return year_of_birth > 1960
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Nieprawidłowa wartość kwoty")
        if amount > self.balance:
            raise ValueError("Brak środków")
        else:
            self.balance -= amount
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Nieprawidłowa wartość kwoty")
        else:
            self.balance += amount

    def express_transfer(self, amount):
        if amount <= 0:
            raise ValueError("Nieprawidłowa wartość kwoty")
        if amount > self.balance + self.express_transfer_fee:
            raise ValueError("Brak środków")
        else:
            self.balance -= amount + self.express_transfer_fee


class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.balance = 0
        self.express_transfer_fee = 5
        
        if len(nip) != 10:
            self.nip = "Invalid"
        else:
            self.nip = nip