import datetime

# המחלקה הזאת מייצגת חשבון בנק אחד
# כל חשבון יודע את הפרטים שלו ויודע לעשות פעולות על עצמו
class Account:
    def __init__(self, account_number, name, pin, balance=0):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.is_active = True
        self.history = []
        self.failed_attempts = 0
        
            # בודק אם הקוד שהמשתמש הכניס נכון
    # אם טעה 3 פעמים - החשבון ננעל אוטומטית
    def verify_pin(self, pin):
        if self.failed_attempts >= 3:
            self.is_active = False
            return False
        if self.pin == pin:
            self.failed_attempts = 0
            return True
        self.failed_attempts = self.failed_attempts + 1
        return False
    
#  הפקדת כסף - מחזיר שני ערכים: הצליח/נכשל + הודעה
    def deposit(self, amount):
        if amount <= 0:
            return False, "Amount must be positive"
        self.balance = self.balance + amount
        self._add_to_history("deposit", amount)
        return True, "Deposit successful"
    
# משיכת כסף - בודק שיש מספיק יתרה לפני המשיכה

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Amount must be positive"
        if amount > self.balance:
            return False, "Not enough balance"
        self.balance = self.balance - amount
        self._add_to_history("withdraw", amount)
        return True, "Withdraw successful"

# בדיקה שה - PIN הישן נכון -> אחכ עושה בדיקה שהוא 4 ספות .    
    def change_pin(self, old_pin, new_pin):
        if old_pin != self.pin:
            return False, "Wrong PIN"
        if len(str(new_pin)) != 4:
            return False, "PIN must be 4 digits"
        self.pin = new_pin
        return True, "PIN changed successfully"
    
    # פונקציה פנימית - מתעדת כל פעולה שקרתה בחשבון
    # שומרת את הסוג, הסכום, התאריך, והיתרה אחרי הפעולה
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

    # ממיר את כל המידע של החשבון ל-dictionary כדי שנוכל לשמור ב-JSON
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "is_active": self.is_active,
            "history": self.history,
            "failed_attempts": self.failed_attempts
        }


# מחלקה שמנהלת את כל החשבונות במערכת - כמו מסד נתונים
class Bank:
    def __init__(self):
        self.accounts = {}  # כל החשבונות נשמרים פה לפי מספר חשבון
        self.admin_password = "admin123"  # TODO: אולי לשמור את זה ב-JSON במקום hardcoded

    # יוצר חשבון חדש ומוסיף ל-dictionary
    def add_account(self, account_number, name, pin, balance=0):
        if account_number in self.accounts:
            return False, "Account already exists"
        new_account = Account(account_number, name, pin, balance)
        self.accounts[account_number] = new_account
        return True, "Account created"

    # מחפש חשבון לפי מספר - מחזיר None אם לא קיים
    def get_account(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        return None

    # העברה בין חשבונות - הפעולה הכי מורכבת כאן
    def transfer(self, from_account, to_number, amount):
        to_account = self.get_account(to_number)
        if to_account is None:
            return False, "Target account not found"
        if not to_account.is_active:
            return False, "Target account is blocked"

        # קודם מנסים למשוך מהשולח
        success, message = from_account.withdraw(amount)
        if not success:
            return False, message

        # אם המשיכה עברה - מפקידים ליעד
        to_account.deposit(amount)
        # NOTE: שומרים היסטוריה בשני הצדדים - גם שולח וגם מקבל
        from_account._add_to_history("transfer_out", amount, to_number)
        to_account._add_to_history("transfer_in", amount, from_account.account_number)
        return True, "Transfer successful"

    # חסימה או שחרור חשבון - מחליף את הסטטוס
    def toggle_account(self, account_number):
        account = self.get_account(account_number)
        if account is None:
            return False, "Account not found"
        account.is_active = not account.is_active
        status = "active" if account.is_active else "blocked"
        return True, "Account is now " + status

    # מחזיר רשימה של כל החשבונות - לשימוש בפאנל מנהל
    def get_all_accounts_info(self):
        result = []
        for number in self.accounts:
            account = self.accounts[number]
            result.append({
                "number": number,
                "name": account.name,
                "balance": account.balance,
                "status": "active" if account.is_active else "blocked"
            })
        return result

