import requests
import pytest
import random

BASE_URL = "http://127.0.0.1:5000"

class TestApiSpeed:
    @pytest.fixture
    def account_data(self):
        data = {
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": str(random.randint(10**10, 10**11 - 1))
        }
        return data

    def test_create_delete_account_speed(self, account_data):
        for i in range(100):
            post_response = requests.post(f"{BASE_URL}/api/accounts", json=account_data, timeout=0.5)
            assert post_response.status_code == 201

            delete_response = requests.delete(f"{BASE_URL}/api/accounts/{account_data['pesel']}", timeout=0.5)
            assert delete_response.status_code == 200

    def test_operation_speed(self, account_data):
        create_response = requests.post(f"{BASE_URL}/api/accounts", json=account_data, timeout=0.5)

        assert create_response.status_code == 201

        for i in range(100):
            response = requests.post(
                f"{BASE_URL}/api/accounts/{account_data['pesel']}/transfer",
                json={"amount": 100, "type": "incoming"},
                timeout=0.5
            )
            assert response.status_code == 200

        get_response = requests.get(f"{BASE_URL}/api/accounts/{account_data['pesel']}")
        assert get_response.status_code == 200
        assert get_response.json()["balance"] == 100*100 

        requests.delete(
            f"{BASE_URL}/api/accounts/{account_data['pesel']}",
            timeout=0.5
        )