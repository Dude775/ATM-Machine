from storage import load_json, write_json
from utils import now_str, secure_random_string


class Account:
    def __init__(self, data):
        self.id = data["id"]
        self.pas = data["pas"]
        self.name = data["name"]
        self.balance = data["balance"]
        self.admin = data["admin"]     
        self.status = data["status"]    
        self.history = data["history"]  

    def to_dict(self):
        return {
            "id": self.id,
            "pas": self.pas,
            "name": self.name,
            "balance": self.balance,
            "admin": self.admin,
            "status": self.status,
            "history": self.history,
        }

    def save(self):
        write_json(self.to_dict())

    def deposit(self, amount: float):
        self.balance += amount
        self.history.append(f"{now_str()} you deposited {amount}")
        self.save()

    def withdraw(self, amount: float) -> bool:
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        self.history.append(f"{now_str()} you withdrew {amount}")
        self.save()
        return True

    def transfer_to(self, other: "Account", amount: float) -> bool:
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        self.history.append(
            f"{now_str()} you sent {amount} to account {other.id}"
        )
        self.save()

        other.balance += amount
        other.history.append(
            f"{now_str()} account {self.id} sent you {amount}"
        )
        other.save()
        return True

    def change_password(self, old, new) -> bool:
        if self.pas != old:
            return False
        self.pas = new
        self.history.append(f"{now_str()} you changed your password")
        self.save()
        return True


class Bank:
    def __init__(self):
        self.accounts = []
        self._load_accounts()

    def _load_accounts(self):
        data = load_json()
        self.accounts = [Account(acc) for acc in data]

    def _save_account(self, acc: Account):
        acc.save()
        self._load_accounts()

    def find_by_id(self, id_):
        for acc in self.accounts:
            if acc.id == id_:
                return acc
        return None

    def login(self, id_, pas):
        for acc in self.accounts:
            if acc.id == id_ and acc.pas == pas:
                return acc
        return None

    def create_account(self, id_, name, is_admin: bool):
        if self.find_by_id(id_) is not None:
            return None, "Account with this ID already exists"

        pas = secure_random_string()
        data = {
            "id": id_,
            "pas": pas,
            "name": name,
            "balance": 0.0,
            "admin": "true" if is_admin else "false",
            "status": "enable",
            "history": [],
        }
        acc = Account(data)
        acc.save()
        self._load_accounts()
        return acc, pas

    def disable_account(self, id_, name):
        acc = self.find_by_id(id_)
        if not acc or acc.name != name:
            return False, "Account not found"
        if acc.admin == "true":
            return False, "Admin can't disable itself"
        acc.status = "disable"
        acc.save()
        return True, "Account disabled"

    def enable_account(self, id_, name):
        acc = self.find_by_id(id_)
        if not acc or acc.name != name:
            return False, "Account not found"
        acc.status = "enable"
        acc.save()
        return True, "Account enabled"

    def all_accounts(self):
        self._load_accounts()
        return self.accounts
