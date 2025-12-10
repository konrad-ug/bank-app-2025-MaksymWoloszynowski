from src.account import BusinessAccount
import pytest

class TestCompanyLoan:
    @pytest.fixture
    def business_account(self, mocker):
        mock_get = mocker.patch("src.account.requests.get")
        mock_get.return_value.json.return_value = {"result": {"subject": {"statusVat": "Czynny"}}}
        business_account = BusinessAccount("Coca Cola", "1234567890")
        return business_account
    
    company_loan_tests = [
        ([4000, -1775, 2000], 4000, 2000, True, 6000),
        ([5000, -1775, -1000, 3000], 6000, 2500, True, 8500),
        ([3000, -1000, -1775], 3000, 5000, False, 3000),
        ([6000, -1000, 4000], 6000, 4000, False, 6000),
    ]

    ids = [
        "sufficient balance and ZUS payment",
        "sufficient balance and ZUS payment with multiple transactions",
        "insufficient balance",
        "no ZUS payment"
    ]

    @pytest.mark.parametrize("history, balance, amount, expected_result, expected_balance", company_loan_tests, ids=ids)
    
    def test_business_loan(self, history, balance, amount, expected_result, expected_balance, business_account):
        business_account.history = history
        business_account.balance = balance
        result = business_account.take_loan(amount)
        assert result == expected_result
        assert business_account.balance == expected_balance
