from src.account import PersonalAccount
import pytest

class TestAccount:
    def test_loan_not_enough_transactions(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.history = [100,200]
        account.balance += sum(account.history)
        prev_account_balance = account.balance
        assert account.submit_for_loan(200) == False
        assert account.balance == prev_account_balance
    
    def test_loan_negative_amount(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        with pytest.raises(ValueError):
            account.submit_for_loan(-200)

    def test_loan_last_three_positive(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.history = [100,200,300]
        account.balance += sum(account.history)
        prev_account_balance = account.balance
        assert account.submit_for_loan(200) == True
        assert account.balance == prev_account_balance + 200
    
    def test_loan_last_three_negative(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.history = [100,200,-300]
        account.balance += sum(account.history)
        prev_account_balance = account.balance
        assert account.submit_for_loan(200) == False
        assert account.balance == prev_account_balance

    def test_loan_last_five_positive(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.history = [100,200,300,400,-100,200]
        account.balance += sum(account.history)
        prev_account_balance = account.balance
        assert account.submit_for_loan(200) == True
        assert account.balance == prev_account_balance + 200

    def test_loan_last_five_negative(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.history = [100,200,300,400,-10000,200]
        account.balance += sum(account.history)
        prev_account_balance = account.balance
        assert account.submit_for_loan(200) == False
        assert account.balance == prev_account_balance

    