from behave import *
import requests

URL = "http://localhost:5000"

@step('I make "{transfer_type}" transfer of "{amount}" from pesel "{pesel}"')
def make_transfer(context, transfer_type, amount, pesel):
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json = {"type": transfer_type ,"amount": float(amount)})
    context.transfer_status_code = response.status_code

@then('The balance of account with pesel "{pesel}" should be "{amount}"')
def check_account_balance(context, pesel, amount):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    account = response.json()
    assert response.status_code == 200
    assert account["balance"] == float(amount)

@then('The transfer should be accepted')
def transfer_accepted(context):
    assert context.transfer_status_code == 200

@then('The transfer should be rejected')
def transfer_rejected(context):
    assert context.transfer_status_code == 422