import tkinter as tk
from tkinter import messagebox
from storage import save_data


class ATMApp:
    def __init__(self, root, bank):
        self.root = root
        self.bank = bank
        self.current_account = None

        self.root.title("ATM Machine")
        self.root.geometry("400x500")
        self.root.configure(bg="#1a237e")

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="ATM Machine", font=("Segoe UI", 24, "bold"),
                 bg="#1a237e", fg="white").pack(pady=30)

        tk.Label(self.root, text="Account Number:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)
        self.acc_entry = tk.Entry(self.root, font=("Segoe UI", 14), justify="center")
        self.acc_entry.pack(pady=5)

        tk.Label(self.root, text="PIN:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)
        self.pin_entry = tk.Entry(self.root, font=("Segoe UI", 14), justify="center", show="*")
        self.pin_entry.pack(pady=5)

        tk.Button(self.root, text="Login", font=("Segoe UI", 14),
                  bg="#4caf50", fg="white", width=15,
                  command=self.handle_login).pack(pady=15)

        tk.Button(self.root, text="Admin", font=("Segoe UI", 14),
                  bg="#f44336", fg="white", width=15,
                  command=self.handle_admin_login).pack(pady=5)

    def handle_login(self):
        acc_number = self.acc_entry.get()
        pin = self.pin_entry.get()

        account = self.bank.get_account(acc_number)
        if account is None:
            messagebox.showerror("Error", "Account not found")
            return
        if not account.is_active:
            messagebox.showerror("Error", "Account is blocked")
            return
        if not account.verify_pin(pin):
            save_data(self.bank)
            messagebox.showerror("Error", "Wrong PIN")
            return

        self.current_account = account
        self.show_user_menu()

    def handle_admin_login(self):
        pass

    def show_user_menu(self):
        self.clear_screen()

        name = self.current_account.name
        balance = self.current_account.balance

        tk.Label(self.root, text=f"Welcome, {name}", font=("Segoe UI", 20, "bold"),
                 bg="#1a237e", fg="white").pack(pady=10)

        tk.Label(self.root, text=f"Balance: {balance}", font=("Segoe UI", 16),
                 bg="#1a237e", fg="#4caf50").pack(pady=5)

        buttons = [
            ("Deposit", self.show_deposit),
            ("Withdraw", self.show_withdraw),
            ("Transfer", self.show_transfer),
            ("History", self.show_history),
            ("Change PIN", self.show_change_pin),
            ("Logout", self.show_login_screen)
        ]

        for text, command in buttons:
            tk.Button(self.root, text=text, font=("Segoe UI", 13),
                      bg="white", fg="#1a237e", width=20,
                      command=command).pack(pady=5)

    def show_deposit(self):
        pass

    def show_withdraw(self):
        pass

    def show_transfer(self):
        pass

    def show_history(self):
        pass

    def show_change_pin(self):
        pass
