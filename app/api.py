from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account registry: {data}")

    account = registry.get_account_by_pesel(data['pesel'])
    if account:
        return jsonify({"message": "Account with that pesel alredy existing"}), 409
    else:
        account = PersonalAccount(data['name'], data['surname'], data['pesel'])
        registry.add_account(account)
        return jsonify({"message": "Account created"}), 201

@app.route('/api/accounts', methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [{"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route('/api/accounts/count', methods=['GET'])
def get_account_count():
    print("Get account count request received")
    count = registry.get_account_count()
    return jsonify({"count": count}), 200
    
@app.route('/api/accounts/<pesel>', methods=['GET'])
def get_account_by_pesel(pesel):
    print("Get account by pesel request received")
    account = registry.get_account_by_pesel(pesel)
    if account:
        account_data = {"name": account.first_name, "surname": account.last_name, "pesel": account.pesel, "balance": account.balance}
        return jsonify(account_data), 200
        
    return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = registry.get_account_by_pesel(pesel)

    if account:
        if "name" in data:
            account.first_name = data["name"]
        if "surname" in data:
            account.last_name = data["surname"]
        return jsonify({"message": "Account updated"}), 200
    
    return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.get_account_by_pesel(pesel)

    if account:
        registry.accounts.remove(account)
        return jsonify({"message": "Account deleted"}), 200
    
    return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    body = request.get_json()
    print(f"Transfer: {body}")

    type = body["type"]
    amount = body["amount"]

    account = registry.get_account_by_pesel(pesel)

    print(registry.accounts[0].pesel)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    match type:
        case "incoming":
            success = account.deposit(amount)
        case "outgoing":
            success = account.withdraw(amount)
        case "express":
            success = account.express_transfer(amount)
        case _:
            return jsonify({"message": "Nieznany typ przelewu"}), 400

    if success:
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    else:
        return jsonify({"message": "Zlecenie nieudane"}), 422
    
    