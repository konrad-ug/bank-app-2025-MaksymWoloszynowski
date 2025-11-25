from src.account import PersonalAccount

class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "49071512368")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0
        assert account.pesel == "49071512368"

    def test_account_creation_too_short_pesel(self):
        account = PersonalAccount("John", "Doe", "490715123")
        assert account.pesel == "Invalid"

    def test_account_creation_too_long_pesel(self):
        account = PersonalAccount("John", "Doe", "49071512328142314")
        assert account.pesel == "Invalid"
    
    def test_account_creation_no_promo_code(self):
        account = PersonalAccount("John", "Doe", "49071512368", promo_code=None)
        assert account.balance == 0
     
    def test_account_creation_invalid_promo_code(self):
        account = PersonalAccount("John", "Doe", "49071512368", promo_code="promo123")
        assert account.balance == 0

    def test_after_1960_2000_valid_pesel_promo_code_bonus(self):
        account = PersonalAccount("John", "Doe", "05271512342", promo_code="PROM_2025")
        assert account.balance == 50

    def test_after_1960_2100_valid_pesel_promo_code_bonus(self):
        account = PersonalAccount("John", "Doe", "05415512342", promo_code="PROM_2025")
        assert account.balance == 50

    def test_after_1960_2200_valid_pesel_promo_code_bonus(self):
        account = PersonalAccount("John", "Doe", "05701512342", promo_code="PROM_2025")
        assert account.balance == 50

    def test_after_1960_invalid_pesel_promo_code_bonus(self):
        account = PersonalAccount("John", "Doe", "05271512342rwef", promo_code="PROM_2025")
        assert account.balance == 0

    def test_1960_promo_code_bonus(self):
        account = PersonalAccount("John", "Doe", "60071512368", promo_code="PROM_2025")
        assert account.balance == 0
    
    def test_before_1960_old_promo_code_bonus(self):
        account = PersonalAccount("John", "Doe", "49071512368", promo_code="PROM_2025")
        assert account.balance == 0