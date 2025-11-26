from src.account_registry import AccountRegistry
from src.account import PersonalAccount
import pytest

class TestAccountRegistry:
    @pytest.fixture
    def registry(self):
        return AccountRegistry()
    
    def test_add_and_get_account(self, registry: AccountRegistry):
        account = PersonalAccount("John", "Doe", "49071512368")
        registry.add_account(account)
        retrieved_account = registry.get_account_by_pesel("49071512368")
        assert retrieved_account == account

    def test_get_account_not_found(self, registry: AccountRegistry):
        retrieved_account = registry.get_account_by_pesel("0000000000")
        assert retrieved_account is None

    def test_get_all_accounts(self, registry: AccountRegistry):
        account1 = PersonalAccount("John", "Doe", "49071512368")
        account2 = PersonalAccount("John", "Doe", "49071512367")
        registry.add_account(account1)
        registry.add_account(account2)
        all_accounts = registry.get_all_accounts()
        assert all_accounts == [account1, account2]

    def test_get_account_count(self, registry: AccountRegistry):
        account1 = PersonalAccount("John", "Doe", "49071512368")
        account2 = PersonalAccount("John", "Doe", "49071512367")
        registry.add_account(account1)
        registry.add_account(account2)
        account_count = registry.get_account_count()
        assert account_count == 2

    