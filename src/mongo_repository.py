from pymongo import MongoClient
from src.account import PersonalAccount

class MongoAccountsRepository:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['bank_db']
        self.collection = self.db['accounts']

    def save_all(self, accounts):
        self.collection.delete_many({})
        for account in accounts:
            self.collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()}
            )
    
    def load_all(self):
        accounts = []
        for data in self.collection.find():
            account = PersonalAccount(first_name=data["first_name"], last_name=data["last_name"], pesel=data["pesel"], promo_code=data["promo_code"])
            account.balance = data["balance"]
            account.history = data["history"]
            accounts.append(account)
    
        return accounts