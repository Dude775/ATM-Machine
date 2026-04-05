import tkinter as tk

# תפריט ראשי של המשתמש אחרי התחברות
class UserMenuScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg="#1a237e")
        self.app = app

        name = self.app.current_account.name
        balance = self.app.current_account.balance

        tk.Label(self, text="Welcome, " + name, font=("Segoe UI", 20, "bold"),
                 bg="#1a237e", fg="white").pack(pady=10)

        self.balance_label = tk.Label(self, text="Balance: " + str(balance),
                 font=("Segoe UI", 16), bg="#1a237e", fg="#4caf50")
        self.balance_label.pack(pady=5)

        buttons = [
            ("Deposit", lambda: self.app.show_screen("deposit")),
            ("Withdraw", lambda: self.app.show_screen("withdraw")),
            ("Transfer", lambda: self.app.show_screen("transfer")),
            ("History", lambda: self.app.show_screen("history")),
            ("Change PIN", lambda: self.app.show_screen("change_pin")),
            ("Logout", self.app.logout)
        ]

        for text, command in buttons:
            tk.Button(self, text=text, font=("Segoe UI", 13),
                      bg="white", fg="#1a237e", width=20,
                      command=command).pack(pady=5)
