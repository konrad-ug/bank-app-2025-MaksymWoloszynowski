import pytest, requests
from src.account import PersonalAccount
from src.mongo_repository import MongoAccountsRepository
from app.api import app, registry

repository = MongoAccountsRepository()
BASE_URL = "http://127.0.0.1:5000"

class TestMongoAPI:
    @pytest.fixture
    def accounts(self):
        account1 = PersonalAccount("Jan", "Kowalski", "49071512368")
        account2 = PersonalAccount("Janina", "Kowalska", "49071512367")
        return [account1, account2]

    def test_save_all_accounts(self, accounts):
        for acc in accounts:
            registry.add_account(acc)
            registry.add_account(acc)

        response = requests.post(f"{BASE_URL}/api/accounts/save")

        assert response.status_code == 200
        assert response.json()["message"] == "Accounts saved"

    def test_load_all_accounts(self):
        response = requests.post(f"{BASE_URL}/api/accounts/load")

        assert response.status_code == 200
        assert response.json()["message"] == "Accounts loaded"
