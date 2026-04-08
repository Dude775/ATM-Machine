import json
import os
from models import Account

DATA_FILE = "data.json"


# save evrything to file
def save_data(bank):
    data = {
        "admin_password": bank.admin_password,
        "accounts": {}
    }
    for number in bank.accounts:
        data["accounts"][number] = bank.accounts[number].to_dict()

    file = None
    try:
        file = open(DATA_FILE, "w", encoding="utf-8")
        json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"שגיאה בשמירה: {e}")
    finally:
        if file:
            file.close()


def load_data(bank):
    if not os.path.exists(DATA_FILE):
        return

    file = None
    try:
        file = open(DATA_FILE, "r", encoding="utf-8")
        data = json.load(file)
    except Exception as e:
        print(f"שגיאה בטעינה: {e}")
        return
    finally:
        if file:
            file.close()

    bank.admin_password = data.get("admin_password", "admin123")

    for number in data.get("accounts", {}):
        acc_data = data["accounts"][number]
        account = Account(
            acc_data["account_number"],
            acc_data["name"],
            acc_data["pin"],
            acc_data.get("balance", 0),
            phone=acc_data.get("phone", ""),
            email=acc_data.get("email", ""),
            id_number=acc_data.get("id_number", ""),
            address=acc_data.get("address", ""),
            status=acc_data.get("status", "active" if acc_data.get("is_active", True) else "blocked")
        )
        account.history = acc_data.get("history", [])
        account.failed_attempts = acc_data.get("failed_attempts", 0)
        bank.accounts[number] = account
