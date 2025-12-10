from src.account import BusinessAccount
import pytest

class TestCompanyTransfer:
    @pytest.fixture
    def business_account(self, mocker):
        mock_get = mocker.patch("src.account.requests.get")
        mock_get.return_value.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        business_account = BusinessAccount("Coca Cola", "1234567890")
        return business_account

    def test_business_account_express_transfer(self, business_account: BusinessAccount):
        business_account.balance = 100
        business_account.express_transfer(50)
        assert business_account.balance == 100 - 50 - business_account.express_transfer_fee
    
    def test_business_account_express_transfer_below_0_acceptable(self, business_account: BusinessAccount):
        business_account.balance = 50
        business_account.express_transfer(50)
        assert business_account.balance == - business_account.express_transfer_fee

    def test_business_account_express_transfer_below_0_too_much(self, business_account: BusinessAccount):
        business_account.balance = 50
        assert business_account.express_transfer(100) == False
