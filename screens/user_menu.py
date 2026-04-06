import tkinter as tk
from styles import COLORS, FONT_TITLE, FONT_SUBTITLE, FONT_BUTTON

# תפריט ראשי של המשתמש
class UserMenuScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg=COLORS["bg"])
        self.app = app
        self.account = app.current_account

        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        # שם משתמש
        tk.Label(center, text="Welcome, " + self.account.name,
                 font=FONT_TITLE, bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 5))

        # קו הפרדה
        tk.Frame(center, bg=COLORS["gold"], height=3, width=200).pack(pady=(0, 10))

        # יתרה
        self.balance_label = tk.Label(center,
                 text="Balance: $" + str(self.account.balance),
                 font=FONT_SUBTITLE, bg=COLORS["bg"], fg=COLORS["green"])
        self.balance_label.pack(pady=(0, 25))

        # כפתורים - רשימה של שם + מסך + צבע
        buttons = [
            ("Deposit", "deposit", COLORS["green"]),
            ("Withdraw", "withdraw", COLORS["red"]),
            ("Transfer", "transfer", COLORS["orange"]),
            ("History", "history", COLORS["bg_light"]),
            ("Change PIN", "change_pin", COLORS["bg_light"]),
        ]

        for text, screen, color in buttons:
            tk.Button(center, text=text, font=FONT_BUTTON,
                      bg=color, fg=COLORS["white"], width=22,
                      relief="flat", cursor="hand2",
                      command=lambda s=screen: self.app.show_screen(s)).pack(pady=4, ipady=3)

        # logout בנפרד
        tk.Button(center, text="Logout", font=("Segoe UI", 11),
                  bg=COLORS["bg"], fg=COLORS["red"], width=22,
                  relief="flat", cursor="hand2", bd=0,
                  command=self.app.logout).pack(pady=(15, 0))
