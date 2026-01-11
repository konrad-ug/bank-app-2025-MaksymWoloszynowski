import requests, pytest, random

BASE_URL = "http://127.0.0.1:5000"

class TestApiCRUD:
    @pytest.fixture
    def data(self):
        data = {
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": str(random.randint(10**10, 10**11 - 1))
        }

        requests.post(f"{BASE_URL}/api/accounts", json=data)

        return data
    
    def test_create_account(self, data):
        pesel = data["pesel"]
        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
        assert response.status_code == 200

    def test_create_account_already_existing(self):
        pesel = str(random.randint(10**10, 10**11 - 1))
        data = {"name": "Jan", "surname": "Kowalski", "pesel": pesel}

        first = requests.post(f"{BASE_URL}/api/accounts", json=data)
        assert first.status_code == 201

        second = requests.post(f"{BASE_URL}/api/accounts", json=data)
        assert second.status_code == 409

    def test_get_account_by_pesel_existing(self, data):
        pesel = data["pesel"]
        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")

        expected_result = {
            "balance": 0,
            "name": data["name"],
            "pesel": data["pesel"],
            "surname": data["surname"]
        }

        assert response.status_code == 200
        assert response.json() == expected_result

    def test_get_account_by_pesel_not_existing(self):
        response = requests.get(f'{BASE_URL}/api/accounts/00000000000')

        assert response.status_code == 404
        assert response.json()['message'] == 'Account not found'
    
    def test_update_account(self, data):
        pesel = data["pesel"]
        update_data = {"name": "Zbigniew"}
        response = requests.patch(f"{BASE_URL}/api/accounts/{pesel}", json=update_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"

        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
        assert response.json()["name"] == "Zbigniew"

    def test_delete_account(self, data):
        pesel = data["pesel"]
        response = requests.delete(f'http://127.0.0.1:5000/api/accounts/{pesel}')

        assert response.status_code == 200
        assert response.json()['message'] == 'Account deleted'