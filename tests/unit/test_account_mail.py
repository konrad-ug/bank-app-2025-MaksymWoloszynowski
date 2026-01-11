from src.account import PersonalAccount, BusinessAccount
from datetime import datetime
import pytest

class TestAccountEmail:
    @pytest.fixture
    def personal_account(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        return account
    
    @pytest.fixture
    def company_account(self, mocker):
        mocker.patch(
            "src.account.BusinessAccount.check_nip",
            return_value=True
        )
        account = BusinessAccount("Coca Cola", "1234567890")
        return account

    def test_send_history_via_email_personal_account_success(self, personal_account, mocker):
        email = "john.doe@gmail.com"
        personal_account.history = [100, -50, 200]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=True)

        result = personal_account.send_history_via_email(email)

        assert result is True
        mock_send.assert_called_once()

        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email_address = mock_send.call_args[0][2]

        assert subject == f"Account Transfer History {datetime.now().date()}"
        assert text == f"Personal account history: {personal_account.history}"
        assert email_address == email

    def test_send_history_via_email_personal_account_failure(self, personal_account, mocker):
        email = "john.doe@gmail.com"
        personal_account.history = [100, -50, 200]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=False)

        result = personal_account.send_history_via_email(email)

        assert result is False
        mock_send.assert_called_once()

    def test_send_history_via_email_company_account_success(self, company_account, mocker):
        email = "coca.cola@gmail.com"
        company_account.history = [100, -50, 200]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=True)

        result = company_account.send_history_via_email(email)

        assert result is True
        mock_send.assert_called_once()

        subject = mock_send.call_args[0][0]
        text = mock_send.call_args[0][1]
        email_address = mock_send.call_args[0][2]

        assert subject == f"Account Transfer History {datetime.now().date()}"
        assert text == f"Company account history: {company_account.history}"
        assert email_address == email

    def test_send_history_via_email_company_account_failure(self, company_account, mocker):
        email = "coca.cola@gmail.com"
        company_account.history = [100, -50, 200]
        mock_send = mocker.patch("src.account.SMTPClient.send", return_value=False)

        result = company_account.send_history_via_email(email)
        assert result is False

        mock_send.assert_called_once()
    