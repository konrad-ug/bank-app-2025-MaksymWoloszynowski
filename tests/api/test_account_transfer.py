import requests, pytest, random
from app.api import registry

BASE_URL = "http://127.0.0.1:5000"

class TestApiTransfer:
    @pytest.fixture
    def data(self):
        data = {
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": str(random.randint(10**10, 10**11 - 1))
        }

        requests.post(f"{BASE_URL}/api/accounts", json=data)

        return data
    
    def transfer(self, pesel, amount, transfer_type):
        body = {"amount": amount, "type": transfer_type}
        response = requests.post(f"{BASE_URL}/api/accounts/{pesel}/transfer", json=body)
        return response

    def test_incoming_transfer(self, data):
        pesel = data["pesel"]

        response = self.transfer(pesel, 500, "incoming")
        balance = requests.get(f"{BASE_URL}/api/accounts/{pesel}").json()["balance"]

        assert response.status_code == 200
        assert response.json()['message'] == 'Zlecenie przyjęto do realizacji'
        assert balance == 500

    def test_outgoing_transfer(self, data):
        pesel = data["pesel"]

        self.transfer(pesel, 500, "incoming")

        response = self.transfer(pesel, 200, "outgoing")

        balance = requests.get(f"{BASE_URL}/api/accounts/{pesel}").json()["balance"]

        assert response.status_code == 200
        assert response.json()['message'] == 'Zlecenie przyjęto do realizacji'
        assert balance == 300

    def test_outgoing_transfer_failure(self, data):
        pesel = data["pesel"]
        
        response = self.transfer(pesel, 10000, "outgoing")

        assert response.status_code == 422
        assert response.json()['message'] == 'Zlecenie nieudane'

    

    def test_express_transfer(self, data):
        pesel = data["pesel"]

        self.transfer(pesel, 500, "incoming")

        response = self.transfer(pesel, 200, "express")

        balance = requests.get(f"{BASE_URL}/api/accounts/{pesel}").json()["balance"]

        assert response.status_code == 200
        assert response.json()['message'] == 'Zlecenie przyjęto do realizacji'
        assert balance < 300

    def test_express_transfer_failure(self, data):
        pesel = data["pesel"]

        self.transfer(pesel, 500, "incoming")

        response = self.transfer(pesel, 10000, "express")

        assert response.status_code == 422
        assert response.json()['message'] == 'Zlecenie nieudane'

    def test_transfer_account_not_found(self):
        pesel = "00000000000000"
        response = self.transfer(pesel, 200, "express")

        assert response.status_code == 404
        assert response.json()['message'] == 'Account not found'

    def test_transfer_unknown_type(self, data):
        pesel = data["pesel"]
        response = self.transfer(pesel, 200, "fbsyufgeryu")

        assert response.status_code == 400
        assert response.json()['message'] == 'Nieznany typ przelewu'