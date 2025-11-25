from src.account import PersonalAccount
import pytest

class TestLoan:
    @pytest.fixture
    def account(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        return account
    
    @pytest.mark.parametrize(("history", "amount", "expected_result", "expected_balance"), [
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