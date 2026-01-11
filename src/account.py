import re
from datetime import date, datetime
import os
import requests
import pytest
from smtp.smtp import SMTPClient

class Account:
    def __init__(self):
        self.balance = 0
        self.history = []
        self.email_message = ""
    
    def withdraw(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            self.history.append(-amount)
            return True
    
    def deposit(self, amount):
        if amount <= 0:
            return False
        else:
            self.balance += amount
            self.history.append(amount)
            return True

    def express_transfer(self, amount):
        if amount <= 0:
            return False
        if amount > self.balance + self.express_transfer_fee:
            return False
        else:
            self.balance -= amount + self.express_transfer_fee
            self.history.append(-amount)
            self.history.append(-self.express_transfer_fee)
            return True
        
    def send_history_via_email(self, email_address):
        return SMTPClient.send(f"Account Transfer History {datetime.now().date()}", f"{self.email_message}: {self.history}", email_address)

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.express_transfer_fee = 1
        self.email_message = "Personal account history"

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
    
    def submit_for_loan(self, amount):
        if amount <= 0:
            raise ValueError("Nieprawidłowa wartość kwoty")

        first_condition = len(self.history) >= 3 and self.history[-1] > 0 and self.history[-2] > 0 and self.history[-3] > 0
        second_condition = len(self.history) >= 5 and sum(self.history[-5:]) > amount
        
        if first_condition or second_condition:
            self.balance += amount
            return True

        return False
    
class BusinessAccount(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.express_transfer_fee = 5
        self.email_message = "Company account history"
        
        if len(nip) != 10:
            self.nip = "Invalid"
        else:
            if self.check_nip(nip):
                self.nip = nip
            else:
                raise ValueError("Company not registered!!")

    def take_loan(self, amount):
        first_condition = self.balance >= 2 * amount
        second_condition = -1775 in self.history

        if first_condition and second_condition:
            self.balance += amount
            return True

        return False 
    
    def check_nip(self, nip):
        gov_url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().isoformat()
        url = f"{gov_url}/api/search/nip/{nip}?date={today}"

        response = requests.get(url)
        data = response.json()

        print("Response od MF: ", data)

        return data['result']['subject']['statusVat'] == "Czynny"