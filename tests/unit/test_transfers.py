from src.account import PersonalAccount, BusinessAccount
import pytest

class TestTransfer:
    def test_withdraw_enough_money(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.deposit(200)
        account.withdraw(100)
        assert account.balance == 100

    def test_withdraw_not_enough_money(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.deposit(50)
        assert account.withdraw(100) == False

    def test_withdraw_incorrect_amount(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        assert account.withdraw(-100) == False

    def test_deposit(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.deposit(100)
        assert account.balance == 100

    def test_deposit_incorrect_amount(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        assert account.deposit(-100) == False
        
    def test_personal_account_express_transfer(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.balance = 100
        account.express_transfer(50)
        assert account.balance == 100 - 50 - account.express_transfer_fee
    
    def test_express_transfer_amount_below_0(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        assert account.express_transfer(-2) == False
    
    def test_personal_account_express_transfer_below_0_acceptable(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.balance = 50
        account.express_transfer(50)
        assert account.balance == - account.express_transfer_fee

    def test_personal_account_express_transfer_below_0_too_much(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        account.balance = 50
        assert account.express_transfer(100) == False

    def test_business_account_express_transfer(self):
        account = BusinessAccount("Coca Cola", "1234567890")
        account.balance = 100
        account.express_transfer(50)
        assert account.balance == 100 - 50 - account.express_transfer_fee
    
    def test_business_account_express_transfer_below_0_acceptable(self):
        account = BusinessAccount("Coca Cola", "1234567890")
        account.balance = 50
        account.express_transfer(50)
        assert account.balance == - account.express_transfer_fee

    def test_business_account_express_transfer_below_0_too_much(self):
        account = BusinessAccount("Coca Cola", "1234567890")
        account.balance = 50
        assert account.express_transfer(100) == False