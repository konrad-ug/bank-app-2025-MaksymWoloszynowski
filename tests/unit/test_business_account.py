from src.account import BusinessAccount
import pytest

class TestBusinessAccount:

    @pytest.fixture
    def valid_nip(self):
        return {
            "result": {
                "subject": {
                    "statusVat": "Czynny"
                }
            }
        }

    @pytest.fixture
    def invalid_nip(self):
        return {
            "result": {
                "subject": {
                    "statusVat": "Zamknięty"
                }
            }
        }

    def test_business_account_create_valid_nip(self, mocker, valid_nip):
        mock_get = mocker.patch("src.account.requests.get")
        mock_get.return_value.json.return_value = valid_nip

        account = BusinessAccount("Coca Cola", "1234567890")

        assert account.company_name == "Coca Cola"
        assert account.nip == "1234567890"

    def test_business_account_create_invalid_nip(self, mocker, invalid_nip):
        mock_get = mocker.patch("src.account.requests.get")
        mock_get.return_value.json.return_value = invalid_nip

        with pytest.raises(ValueError):
            BusinessAccount("Coca Cola", "0000000000")
            
    def test_business_account_create_nip_wrong(self, mocker):
        account = BusinessAccount("Coca Cola", "f")

        assert account.company_name == "Coca Cola"
        assert account.nip == "Invalid"
