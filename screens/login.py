import tkinter as tk
from tkinter import messagebox
import os

# מסך הכניסה - הדבר הראשון שנטען כשפותחים את התוכנה
class LoginScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg="#1a237e")
        self.app = app

        tk.Label(self, text="ATM Machine", font=("Segoe UI", 24, "bold"),
                 bg="#1a237e", fg="white").pack(pady=30)

        # שדה מספר חשבון
        tk.Label(self, text="Account Number:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)
        self.acc_entry = tk.Entry(self, font=("Segoe UI", 14), justify="center")
        self.acc_entry.pack(pady=5)

        # שדה PIN - מוסתר עם כוכביות
        tk.Label(self, text="PIN:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)
        self.pin_entry = tk.Entry(self, font=("Segoe UI", 14), justify="center", show="*")
        self.pin_entry.pack(pady=5)

        tk.Button(self, text="Login", font=("Segoe UI", 14),
                  bg="#4caf50", fg="white", width=15,
                  command=self.handle_login).pack(pady=15)

        tk.Button(self, text="Admin", font=("Segoe UI", 14),
                  bg="#f44336", fg="white", width=15,
                  command=self.handle_admin_login).pack(pady=5)

    # NOTE: סדר הבדיקות חשוב - קודם בודקים אם קיים, אחכ חסום, אחכ PIN
    def handle_login(self):
        acc_number = self.acc_entry.get()
        pin = self.pin_entry.get()

        account = self.app.bank.get_account(acc_number)
        if account is None:
            messagebox.showerror("Error", "Account not found")
            return
        if not account.is_active:
            messagebox.showerror("Error", "Account is blocked")
            return
        if not account.verify_pin(pin):
            self.app.save()
            messagebox.showerror("Error", "Wrong PIN")
            return

        self.app.current_account = account
        self.app.show_screen("user_menu")

    # חלון קופץ לסיסמת מנהל - נשאר popup כי זה חד פעמי
    def handle_admin_login(self):
        self.admin_win = tk.Toplevel(self.app.root)
        self.admin_win.title("Admin Login")
        self.admin_win.geometry("300x200")
        self.admin_win.configure(bg="#1a237e")

        tk.Label(self.admin_win, text="Admin Password:",
                 font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=10)

        self.admin_pass_entry = tk.Entry(self.admin_win,
                                         font=("Segoe UI", 14), justify="center", show="*")
        self.admin_pass_entry.pack(pady=5)

        tk.Button(self.admin_win, text="Login", font=("Segoe UI", 13),
                  bg="#f44336", fg="white", width=15,
                  command=self.check_admin_password).pack(pady=15)

    def check_admin_password(self):
        password = self.admin_pass_entry.get()
        if password == self.app.bank.admin_password:
            self.admin_win.destroy()
            self.app.show_screen("admin")
        else:
            messagebox.showerror("Error", "Wrong admin password")
