import datetime
import secrets
import string


class BankEntity:
    def __init__(self, name, status="active"):
        self.name = name
        self.status = status

    @property
    def is_active(self):
        return self.status != "disable"


class Account(BankEntity):
    def __init__(self, account_number, pin, name, balance=0, admin="false",
                 status="enable", history=None, failed_attempts=0):
        super().__init__(name, status)
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.admin = admin
        self.history = history if history is not None else []
        self.failed_attempts = failed_attempts

    def add_to_history(self, log):
        self.history.append(log)

    def verify_pin(self, pin):
        return self.pin == pin

    def deposit(self, amount):
        try:
            float(amount)
        except ValueError:
            return "enter only numbers please"
        if float(amount) < 0:
            return "You cannot tpye negative numbers"
        self.balance += float(amount)
        x = datetime.datetime.now()
        log = f"{x.strftime('%c')} you deposite {float(amount)}"
        self.add_to_history(log)
        return "operation success!"

    def withdraw(self, amount):
        try:
            float(amount)
        except ValueError:
            return "enter only numbers please"
        if float(amount) < 0:
            return "You cannot tpye negative numbers"
        if self.balance - float(amount) < 0:
            return "you dont have enough money"
        self.balance -= float(amount)
        x = datetime.datetime.now()
        log = f"{x.strftime('%c')} you withdraw {float(amount)}"
        self.add_to_history(log)
        return "operation success!"

    def transfer_out(self, amount, target_account):
        try:
            float(amount)
        except ValueError:
            return "enter only numbers please"
        if float(amount) < 0:
            return "You cannot tpye negative numbers"
        if target_account.account_number == self.account_number:
            return "you can't transfer to your account"
        if self.balance - float(amount) < 0:
            return "you dont have enough money"
        self.balance -= float(amount)
        x = datetime.datetime.now()
        log = f"{x.strftime('%c')} you send to account {target_account.account_number} {float(amount)}"
        self.add_to_history(log)
        target_account.balance += float(amount)
        log = f"{x.strftime('%c')} account {self.account_number} send to you {float(amount)}"
        target_account.add_to_history(log)
        return "operation success!"

    def change_pin(self, old, pas, pasv):
        if old != self.pin:
            return "old password incorrect"
        if pas != pasv:
            return "password don't match"
        if len(pas) < 8:
            return "password must containe 8 characters"
        self.pin = pas
        return "operation success!"

    def to_dict(self):
        return {
            "id": self.account_number,
            "pas": self.pin,
            "name": self.name,
            "balance": self.balance,
            "admin": self.admin,
            "status": self.status,
            "attempt": self.failed_attempts,
            "history": self.history,
        }


class Bank:
    def __init__(self):
        self.accounts = {}
        self.admin_password = None

    def _secure_random_string(self, length=16):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def add_account(self, admin, name, account_number):
        if account_number in self.accounts:
            return "already have accound with the same id"
        if len(account_number) < 6:
            return "id must containe 6 characters"
        if len(name) < 4:
            return "name must containe 4 characters"
        if admin != "y" and admin != "n":
            return "you must enter y/n!"
        admin_value = "true" if admin == "y" else "false"
        pin = self._secure_random_string()
        new_account = Account(
            account_number=account_number,
            pin=pin,
            name=name,
            balance=0,
            admin=admin_value,
            status="enable",
            history=[],
            failed_attempts=0,
        )
        self.accounts[account_number] = new_account
        return "success!\nuser password: " + pin

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def remove_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]

    def transfer(self, source_account, amount, target_account_number):
        target = self.get_account(target_account_number)
        if target is None:
            return "account don't found!"
        return source_account.transfer_out(amount, target)

    def toggle_account(self, name, account_number, action):
        account = self.get_account(account_number)
        if account is None or account.name != name:
            return "account don't found!"
        if action == "disable":
            if account.admin == "false":
                account.status = "disable"
                return "Account disable!"
            return "Admin can't disable itself!!"
        if action == "enable":
            account.status = "enable"
            account.failed_attempts = 0
            return "Account enable!"
        return "account don't found!"

    def get_all_accounts_info(self):
        result = []
        num = 1
        for account in self.accounts.values():
            result.append(
                f"{num}: Name = {account.name}, ID = {account.account_number}, Status = {account.status}, Balance = {account.balance:,}, Admin = {account.admin}"
            )
            num += 1
        return result

    def login_user(self, account_number, pin):
        account = self.get_account(account_number)
        if account is None:
            return None
        if account.verify_pin(pin):
            if account.failed_attempts < 3 and account.status != "disable":
                account.failed_attempts = 0
        else:
            account.failed_attempts += 1
        return account
