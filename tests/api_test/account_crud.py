import requests

BASE_URL = "http://127.0.0.1:5000"

class TestApiCRUD:
    def create_account(self):
        data = {
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": "12345678901"
        }

        response = requests.post(f"{BASE_URL}/api/accounts", json=data)
        assert response.status_code == 201
        return "12345678901"
    
    def test_create_account(self):
        pesel = self.create_account()
        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
        assert response.status_code == 200

    def test_get_account_by_pesel_existing(self):
        pesel = self.create_account()
        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")

        expected_result = {
            "balance": 0,
            "name": "Jan",
            "pesel": "12345678901",
            "surname": "Kowalski"
        }

        assert response.status_code == 200
        assert response.json() == expected_result

    def test_get_account_by_pesel_not_existing(self):
        response = requests.get('http://127.0.0.1:5000/api/accounts/00000000000')

        assert response.status_code == 404
        assert response.json()['message'] == 'Account not found'
    
    def test_update_account(self):
        pesel = self.create_account()
        update_data = {"name": "Zbigniew"}
        response = requests.patch(f"{BASE_URL}/api/accounts/{pesel}", json=update_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"

        response = requests.get(f"{BASE_URL}/api/accounts/{pesel}")
        assert response.json()["name"] == "Zbigniew"

    def test_delete_account(self):
        pesel = self.create_account()
        response = requests.delete(f'http://127.0.0.1:5000/api/accounts/{pesel}')

        assert response.status_code == 200
        assert response.json()['message'] == 'Account deleted'