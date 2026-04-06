import tkinter as tk
from models import Bank
from storage import load_data, save_data
from styles import COLORS, FONT_LABEL
import datetime

# האפליקציה הראשית - מנהלת את כל המסכים בחלון אחד
class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Machine")
        self.root.geometry("550x650")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(True, True)
        # גודל מינימלי שלא ישבור את העיצוב
        self.root.minsize(450, 550)

        self.bank = Bank()
        load_data(self.bank)

        self.current_account = None
        self.current_frame = None

        # --- header קבוע למעלה ---
        self.header = tk.Frame(self.root, bg="#0d1442", height=40)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # שעון בצד שמאל
        self.clock_label = tk.Label(self.header, text="", font=("Consolas", 10),
                                    bg="#0d1442", fg=COLORS["gold"])
        self.clock_label.pack(side="left", padx=10)

        # שם משתמש + יתרה בצד ימין
        self.user_label = tk.Label(self.header, text="", font=("Segoe UI", 10),
                                   bg="#0d1442", fg=COLORS["green"])
        self.user_label.pack(side="right", padx=10)

        # שם האפליקציה באמצע
        tk.Label(self.header, text="ID Bank", font=("Segoe UI", 11, "bold"),
                 bg="#0d1442", fg=COLORS["white"]).pack(side="left", expand=True)

        # container למסכים - מתחת ל-header
        self.container = tk.Frame(self.root, bg=COLORS["bg"])
        self.container.pack(fill="both", expand=True)

        # מפעיל את השעון
        self.update_clock()

        self.show_screen("login")

    # שעון שמתעדכן כל שניה
    def update_clock(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%d/%m/%Y")
        self.clock_label.config(text=time_str + "  |  " + date_str)
        # קורא לעצמו שוב אחרי 1000 מילישניות
        self.root.after(1000, self.update_clock)

    # מעדכן את ה-header עם פרטי המשתמש
    def update_header(self):
        if self.current_account:
            text = self.current_account.name + "  |  $" + str(self.current_account.balance)
            self.user_label.config(text=text, fg=COLORS["green"])
        else:
            self.user_label.config(text="")

    # מחליף את המסך הנוכחי
    def show_screen(self, screen_name, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.update_header()

        if screen_name == "login":
            from screens.login import LoginScreen
            self.current_frame = LoginScreen(self.container, self)
        elif screen_name == "user_menu":
            from screens.user_menu import UserMenuScreen
            self.current_frame = UserMenuScreen(self.container, self)
        elif screen_name == "deposit":
            from screens.deposit import DepositScreen
            self.current_frame = DepositScreen(self.container, self)
        elif screen_name == "withdraw":
            from screens.withdraw import WithdrawScreen
            self.current_frame = WithdrawScreen(self.container, self)
        elif screen_name == "transfer":
            from screens.transfer import TransferScreen
            self.current_frame = TransferScreen(self.container, self)
        elif screen_name == "history":
            from screens.history import HistoryScreen
            self.current_frame = HistoryScreen(self.container, self)
        elif screen_name == "change_pin":
            from screens.change_pin import ChangePinScreen
            self.current_frame = ChangePinScreen(self.container, self)
        elif screen_name == "admin":
            from screens.admin import AdminScreen
            self.current_frame = AdminScreen(self.container, self)

        self.current_frame.pack(fill="both", expand=True)

    # שומר את הנתונים
    def save(self):
        save_data(self.bank)

    # מנקה את המשתמש ומחזיר למסך כניסה
    def logout(self):
        self.current_account = None
        self.show_screen("login")
