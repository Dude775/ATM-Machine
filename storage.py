import json
from models import Account

DATA_FILE = "data.json"


def save_data(bank):
    try:
        accounts_list = [account.to_dict() for account in bank.accounts.values()]
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(accounts_list, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")


def load_data(bank):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            file_data = json.load(file)
        for account_dict in file_data:
            account = Account(
                account_number=account_dict.get("id"),
                pin=account_dict.get("pas"),
                name=account_dict.get("name"),
                balance=account_dict.get("balance", 0),
                admin=account_dict.get("admin", "false"),
                status=account_dict.get("status", "enable"),
                history=account_dict.get("history", []),
                failed_attempts=account_dict.get("attempt", 0),
            )
            bank.accounts[account.account_number] = account
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error loading data: {e}")
