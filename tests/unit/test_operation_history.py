from src.account import Account
import pytest

class TestOperationHistory:
    def test_history_personal_account(self):
        account = Account("John", "Doe", "49071512368")
        account.deposit(500)
        account.express_transfer(300)
        assert account.history == [500,-300,-account.express_transfer_fee]

    def test_history_business_account(self):
        account = Account("John", "Doe", "49071512368")
        account.deposit(500)
        account.express_transfer(300)
        assert account.history == [500,-300,-account.express_transfer_fee]

    def test_failed_transfer(self):
        account = Account("John", "Doe", "49071512368")
        with pytest.raises(ValueError):
            account.withdraw(1000)
        assert account.history == []