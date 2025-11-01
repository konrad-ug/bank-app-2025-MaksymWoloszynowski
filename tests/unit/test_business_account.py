from src.account import BusinessAccount

class TestBusinessAccount:
    def test_business_account_create(self):
        account = BusinessAccount("Coca Cola", "1234567890")
        assert account.company_name == "Coca Cola"
        assert account.nip == "1234567890"

    def test_business_account_create_incorrect_nip(self):
        account = BusinessAccount("Coca Cola", "f")
        assert account.company_name == "Coca Cola"
        assert account.nip == "Invalid"
    