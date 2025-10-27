from src.account import Account, BusinessAccount
import pytest

class TestTransfer:
    def test_withdraw_enough_money(self):
        account = Account("John", "Doe", "49071512368")
        account.deposit(200)
        account.withdraw(100)
        assert account.balance == 100

    def test_withdraw_not_enough_money(self):
        account = Account("John", "Doe", "49071512368")
        account.deposit(50)
        with pytest.raises(ValueError):
            account.withdraw(100)

    def test_withdraw_incorrect_amount(self):
        account = Account("John", "Doe", "49071512368")
        with pytest.raises(ValueError):
            account.withdraw(-100)

    def test_deposit(self):
        account = Account("John", "Doe", "49071512368")
        account.deposit(100)
        assert account.balance == 100

    def test_deposit_incorrect_amount(self):
        account = Account("John", "Doe", "49071512368")
        with pytest.raises(ValueError):
            account.deposit(-100)
        
    def test_personal_account_express_transfer(self):
        account = Account("John", "Doe", "49071512368")
        account.balance = 100
        account.express_transfer(50)
        assert account.balance == 100 - 50 - account.express_transfer_fee
    
    def test_personal_account_express_transfer_below_0_acceptable(self):
        account = Account("John", "Doe", "49071512368")
        account.balance = 50
        account.express_transfer(50)
        assert account.balance == - account.express_transfer_fee

    def test_personal_account_express_transfer_below_0_too_much(self):
        account = Account("John", "Doe", "49071512368")
        account.balance = 50
        with pytest.raises(ValueError):
            account.express_transfer(100)

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
        with pytest.raises(ValueError):
            account.express_transfer(100)