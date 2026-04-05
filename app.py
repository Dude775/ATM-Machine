import tkinter as tk
from models import Bank
from storage import load_data, save_data

# האפליקציה הראשית - מנהלת את כל המסכים בחלון אחד
class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("500x600")
        self.root.configure(bg="#1a237e")
        self.root.resizable(False, False)

        self.bank = Bank()
        load_data(self.bank)

        self.current_account = None
        self.current_frame = None

        # TODO: אולי להוסיף לוגו למעלה
        self.show_screen("login")

    # מחליף את המסך הנוכחי - מוחק את הישן ומציג חדש
    def show_screen(self, screen_name, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        if screen_name == "login":
            from screens.login import LoginScreen
            self.current_frame = LoginScreen(self.root, self)
        elif screen_name == "user_menu":
            from screens.user_menu import UserMenuScreen
            self.current_frame = UserMenuScreen(self.root, self)
        elif screen_name == "deposit":
            from screens.deposit import DepositScreen
            self.current_frame = DepositScreen(self.root, self)
        elif screen_name == "withdraw":
            from screens.withdraw import WithdrawScreen
            self.current_frame = WithdrawScreen(self.root, self)
        elif screen_name == "transfer":
            from screens.transfer import TransferScreen
            self.current_frame = TransferScreen(self.root, self)
        elif screen_name == "history":
            from screens.history import HistoryScreen
            self.current_frame = HistoryScreen(self.root, self)
        elif screen_name == "change_pin":
            from screens.change_pin import ChangePinScreen
            self.current_frame = ChangePinScreen(self.root, self)
        elif screen_name == "admin":
            from screens.admin import AdminScreen
            self.current_frame = AdminScreen(self.root, self)

        self.current_frame.pack(fill="both", expand=True)

    # שומר את הנתונים - כל מסך קורא לזה אחרי פעולה
    def save(self):
        save_data(self.bank)

    # מנקה את המשתמש ומחזיר למסך כניסה
    def logout(self):
        self.current_account = None
        self.show_screen("login")
