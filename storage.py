import json
import os
from models import Account

DATA_FILE = "data.json"


def save_data(bank):
    data = {
        "admin_password": bank.admin_password,
        "accounts": {}
    }
    for number in bank.accounts:
        data["accounts"][number] = bank.accounts[number].to_dict()

    try:
        file = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.close()
    except Exception as e:
        print("Error saving data: " + str(e))


def load_data(bank):
    if not os.path.exists(DATA_FILE):
        return

    try:
        file = open(DATA_FILE, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
    except Exception as e:
        print("Error loading data: " + str(e))
        return

    bank.admin_password = data.get("admin_password", "admin123")

    for number in data.get("accounts", {}):
        acc_data = data["accounts"][number]
        account = Account(
            acc_data["account_number"],
            acc_data["name"],
            acc_data["pin"],
            acc_data["balance"]
        )
        account.is_active = acc_data.get("is_active", True)
        account.history = acc_data.get("history", [])
        account.failed_attempts = acc_data.get("failed_attempts", 0)
        bank.accounts[number] = account
