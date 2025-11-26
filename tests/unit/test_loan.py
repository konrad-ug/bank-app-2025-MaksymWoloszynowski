from src.account import PersonalAccount, BusinessAccount
import pytest

class TestLoan:
    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        return account
    
    @pytest.mark.parametrize("history, amount, expected_result, expected_balance", [
        ([100,200], 200, False, 0),
        ([100,200,300], 200, True, 200),
        ([100,200,-300], 200, False, 0),
        ([100,200,300,400,-100,200], 200, True, 200),
        ([100,200,300,400,-10000,200], 200, False, 0)
    ])

    def test_loan(self, account, history, amount, expected_result, expected_balance):
        account.history = history
        result = account.submit_for_loan(amount)
        assert result == expected_result
        assert account.balance == expected_balance
    
    def test_loan_invalid_amount(self, account):
        with pytest.raises(ValueError):
            account.submit_for_loan(0)

        with pytest.raises(ValueError):
            account.submit_for_loan(-100)

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
    
    def test_business_loan(self, history, balance, amount, expected_result, expected_balance):
        business_account = BusinessAccount("Coca Cola", "1234567890")
        business_account.history = history
        business_account.balance = balance
        result = business_account.take_loan(amount)
        assert result == expected_result
        assert business_account.balance == expected_balance
