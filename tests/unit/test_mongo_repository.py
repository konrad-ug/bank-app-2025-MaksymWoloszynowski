import pytest
from unittest.mock import Mock
from src.account import PersonalAccount
from src.mongo_repository import MongoAccountsRepository

class TestMongoRepository:
    @pytest.fixture
    def account_1(self):
        account = PersonalAccount("Jan", "Kowalski", "49071512368")
        return account
    
    @pytest.fixture
    def account_2(self):
        account = PersonalAccount("Janina", "Kowalska", "49071512367")
        return account

    def test_save_all(self, mocker, account_1, account_2):
        mock_collection = mocker.Mock()
        repo = MongoAccountsRepository()
        repo.collection = mock_collection

        accounts = [account_1, account_2]
        repo.save_all(accounts)

        mock_collection.delete_many.assert_called_once_with({})

        assert mock_collection.update_one.call_count == 2

        first_call = mock_collection.update_one.call_args_list[0][0]
        assert "pesel" in first_call[0]
        assert "$set" in first_call[1]

    def test_load_all(self, mocker, account_1, account_2):
        mock_collection = mocker.Mock()
        mock_collection.find.return_value = [
            account_1.to_dict(),
            account_2.to_dict(),
        ]

        repo = MongoAccountsRepository()
        repo.collection = mock_collection

        accounts = repo.load_all()

        assert len(accounts) == 2
        assert accounts[0].first_name == "Jan"
        assert accounts[0].pesel == "49071512368"
        assert accounts[0].balance == 0

        assert accounts[1].first_name == "Janina"
        assert accounts[1].pesel == "49071512367"
        assert accounts[1].balance == 0