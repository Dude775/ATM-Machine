import datetime


class BankEntity:
    def __init__(self, name, status="active"):
        self.name = name
        self.status = status

    def is_active(self):
        return self.status == "active"


class Account(BankEntity):
    def __init__(self, account_number, name, pin, balance=0,
                 phone="", email="", id_number="", address="", status="active"):
        super().__init__(name, status)
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.phone = phone
        self.email = email
        self.id_number = id_number
        self.address = address
        self.history = []
        self.failed_attempts = 0

    # check if pin is correct, if not add to faild counter
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
        self.add_to_history("deposit", amount)
        return True, f"הופקדו {amount} ₪ בהצלחה"
    def withdraw(self, amount):
        if amount <= 0:
            return False, "הסכום חייב להיות חיובי"
        # bodek im yesh maspik kesef
        if amount > self.balance:
            return False, "אין מספיק כסף בחשבון"
        self.balance -= amount
        self.add_to_history("withdraw", amount)
        return True, f"נמשכו {amount} ₪ בהצלחה"

    def change_pin(self, old_pin, new_pin):
        if old_pin != self.pin:
            return False, "הקוד הישן שגוי"
        if len(str(new_pin)) != 4:
            return False, "קוד PIN חייב להכיל 4 ספרות"
        self.pin = new_pin
        return True, "קוד PIN שונה בהצלחה"
    def add_to_history(self, action_type, amount, target=None):
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
            "address": self.address,
            "status": self.status,
            "history": self.history,
            "failed_attempts": self.failed_attempts
        }


class Bank:
    def __init__(self):
        self.accounts = {}
        self.admin_password = "admin123"

    def add_account(self, account_number, name, pin, balance=0,
                    phone="", email="", id_number="", address="", status="active"):
        if account_number in self.accounts:
            return False, "מספר חשבון כבר קיים"
        if len(str(pin)) != 4:
            return False, "קוד PIN חייב להכיל 4 ספרות"
        if not str(pin).isdigit():
            return False, "קוד PIN חייב להכיל ספרות בלבד"
        new_account = Account(account_number, name, pin, balance,
                              phone, email, id_number, address, status)
        self.accounts[account_number] = new_account
        return True, "חשבון נוצר בהצלחה"

    def get_account(self, account_number):
        acc = self.accounts.get(account_number, None)
        return acc

    def remove_account(self, account_number):
        if account_number not in self.accounts:
            return False, "חשבון לא נמצא"
        del self.accounts[account_number]
        return True, f"חשבון {account_number} נמחק"

    def transfer(self, from_account, to_number, amount):
        to_account = self.get_account(to_number)
        if to_account is None:
            return False, "חשבון היעד לא נמצא"
        if not to_account.is_active():
            return False, "חשבון היעד חסום"
        if amount <= 0:
            return False, "הסכום חייב להיות חיובי"
        if from_account.balance < amount:
            return False, "אין מספיק כסף בחשבון"

        from_account.balance -= amount
        to_account.balance += amount
        from_account.add_to_history("transfer_out", amount, to_number)
        to_account.add_to_history("transfer_in", amount, from_account.account_number)
        return True, f"הועברו {amount} ₪ לחשבון {to_number}"

    # TODO: maybe add email notification later

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
        count = 0
        for a in self.accounts.values():
            if a.status == "pending":
                count += 1
        return count

    def get_system_stats(self):
        total_accounts = len(self.accounts)
        total_balance = 0
        active_count = 0
        blocked_count = 0
        total_transactions = 0
        for acc in self.accounts.values():
            total_balance += acc.balance
            if acc.is_active():
                active_count += 1
            else:
                blocked_count += 1
            total_transactions += len(acc.history)
        return {
            "total_accounts": total_accounts,
            "total_balance": total_balance,
            "active": active_count,
            "blocked": blocked_count,
            "total_transactions": total_transactions
        }

    def search_account(self, q):
        # search by account number first
        acc = self.get_account(q)
        if acc:
            return acc
        # then search by name (partial, case-insensitive)
        for acc in self.accounts.values():
            if q.lower() in acc.name.lower():
                return acc
        return None
