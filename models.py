import datetime


class Account:
    def __init__(self, account_number, name, pin, balance=0,
                 phone="", email="", id_number="", status="active"):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.phone = phone
        self.email = email
        self.id_number = id_number
        self.status = status  # "active" / "blocked" / "pending"
        self.history = []
        self.failed_attempts = 0

    @property
    def is_active(self):
        return self.status == "active"

    def verify_pin(self, pin):
        if self.failed_attempts >= 3:
            self.status = "blocked"
            return False
        if self.pin == pin:
            self.failed_attempts = 0
            return True
        self.failed_attempts += 1
        return False

    def deposit(self, amount):
        if amount <= 0:
            return False, "הסכום חייב להיות חיובי"
        self.balance += amount
        self._add_to_history("deposit", amount)
        return True, f"הופקדו {amount} ₪ בהצלחה"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "הסכום חייב להיות חיובי"
        if amount > self.balance:
            return False, "אין מספיק כסף בחשבון"
        self.balance -= amount
        self._add_to_history("withdraw", amount)
        return True, f"נמשכו {amount} ₪ בהצלחה"

    def change_pin(self, old_pin, new_pin):
        if old_pin != self.pin:
            return False, "הקוד הישן שגוי"
        if len(str(new_pin)) != 4:
            return False, "קוד PIN חייב להכיל 4 ספרות"
        self.pin = new_pin
        return True, "קוד PIN שונה בהצלחה"

    def _add_to_history(self, action_type, amount, target=None):
        record = {
            "type": action_type,
            "amount": amount,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "balance_after": self.balance
        }
        if target:
            record["target"] = target
        self.history.append(record)

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "phone": self.phone,
            "email": self.email,
            "id_number": self.id_number,
            "status": self.status,
            "history": self.history,
            "failed_attempts": self.failed_attempts
        }


class Bank:
    def __init__(self):
        self.accounts = {}
        self.admin_password = "admin123"

    def add_account(self, account_number, name, pin, balance=0,
                    phone="", email="", id_number="", status="active"):
        if account_number in self.accounts:
            return False, "מספר חשבון כבר קיים"
        new_account = Account(account_number, name, pin, balance,
                              phone, email, id_number, status)
        self.accounts[account_number] = new_account
        return True, "חשבון נוצר בהצלחה"

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    def remove_account(self, account_number):
        if account_number not in self.accounts:
            return False, "חשבון לא נמצא"
        del self.accounts[account_number]
        return True, f"חשבון {account_number} נמחק"

    def transfer(self, from_account, to_number, amount):
        to_account = self.get_account(to_number)
        if to_account is None:
            return False, "חשבון היעד לא נמצא"
        if not to_account.is_active:
            return False, "חשבון היעד חסום"
        success, message = from_account.withdraw(amount)
        if not success:
            return False, message
        to_account.deposit(amount)
        from_account._add_to_history("transfer_out", amount, to_number)
        to_account._add_to_history("transfer_in", amount, from_account.account_number)
        return True, f"הועברו {amount} ₪ לחשבון {to_number}"

    def toggle_account(self, account_number):
        account = self.get_account(account_number)
        if account is None:
            return False, "חשבון לא נמצא"
        if account.status == "active":
            account.status = "blocked"
        else:
            account.status = "active"
        return True, f"חשבון {account_number} הוא כעת {account.status}"

    def approve_account(self, account_number):
        account = self.get_account(account_number)
        if account is None:
            return False, "חשבון לא נמצא"
        if account.status != "pending":
            return False, "חשבון לא ממתין לאישור"
        account.status = "active"
        return True, f"חשבון {account_number} אושר בהצלחה"

    def get_all_accounts_info(self):
        result = []
        for number, account in self.accounts.items():
            result.append({
                "number": number,
                "name": account.name,
                "balance": account.balance,
                "status": account.status,
                "phone": account.phone,
                "email": account.email,
                "id_number": account.id_number
            })
        return result

    def get_pending_count(self):
        return sum(1 for a in self.accounts.values() if a.status == "pending")