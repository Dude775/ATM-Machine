import tkinter as tk
from tkinter import messagebox
from storage import save_data


class ATMApp:
    def __init__(self, root, bank):
        self.root = root
        self.bank = bank
        self.current_account = None  # מי שמחובר עכשיו - בהתחלה אף אחד

        self.root.title("ATM Machine")
        self.root.geometry("400x500")
        self.root.configure(bg="#1a237e")

        # מסך ראשון שנטען כשפותחים את התוכנה
        self.show_login_screen()

    # מוחק את כל מה שעל המסך - משתמשים בזה לפני כל מעבר מסך
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------- מסך כניסה --------
    def show_login_screen(self):
        self.clear_screen()
        self.current_account = None  # מנקה את המשתמש המחובר

        tk.Label(self.root, text="ATM Machine", font=("Segoe UI", 24, "bold"),
                 bg="#1a237e", fg="white").pack(pady=30)

        # שדה מספר חשבון
        tk.Label(self.root, text="Account Number:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)
        self.acc_entry = tk.Entry(self.root, font=("Segoe UI", 14), justify="center")
        self.acc_entry.pack(pady=5)

        # שדה PIN - מוסתר עם כוכביות
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

    # בודק את הפרטים שהוזנו ומחליט אם להכניס או לא
    def handle_login(self):
        acc_number = self.acc_entry.get()
        pin = self.pin_entry.get()

        # NOTE: סדר הבדיקות חשוב - קודם בודקים אם קיים, אחכ אם חסום, אחכ PIN
        account = self.bank.get_account(acc_number)
        if account is None:
            messagebox.showerror("Error", "Account not found")
            return
        if not account.is_active:
            messagebox.showerror("Error", "Account is blocked")
            return
        if not account.verify_pin(pin):
            save_data(self.bank)  # שומרים כי מונה הנסיונות עלה
            messagebox.showerror("Error", "Wrong PIN")
            return

        self.current_account = account
        self.show_user_menu()

    # -------- כניסת מנהל --------
    def handle_admin_login(self):
        # חלון קופץ לסיסמת מנהל
        self.admin_login_window = tk.Toplevel(self.root)
        self.admin_login_window.title("Admin Login")
        self.admin_login_window.geometry("300x200")
        self.admin_login_window.configure(bg="#1a237e")

        tk.Label(self.admin_login_window, text="Admin Password:",
                 font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=10)

        self.admin_pass_entry = tk.Entry(self.admin_login_window,
                                         font=("Segoe UI", 14), justify="center", show="*")
        self.admin_pass_entry.pack(pady=5)

        tk.Button(self.admin_login_window, text="Login", font=("Segoe UI", 13),
                  bg="#f44336", fg="white", width=15,
                  command=self.check_admin_password).pack(pady=15)
    # בודק אם הסיסמה נכונה
    def check_admin_password(self):
        password = self.admin_pass_entry.get()
        if password == self.bank.admin_password:
            self.admin_login_window.destroy()
            self.show_admin_menu()
        else:
            messagebox.showerror("Error", "Wrong admin password")
# !  מפה זה כל החלק של תפריט מנהל - UI/UX   
    # -------- תפריט מנהל --------
    def show_admin_menu(self):
        self.clear_screen()

        tk.Label(self.root, text="Admin Panel", font=("Segoe UI", 22, "bold"),
                 bg="#1a237e", fg="white").pack(pady=15)
        buttons = [
            ("Create Account", self.show_create_account),
            ("View All Accounts", self.show_all_accounts),
            ("Block / Unblock Account", self.show_toggle_account),
            ("Logout", self.show_login_screen)
        ]

        for text, command in buttons:
            tk.Button(self.root, text=text, font=("Segoe UI", 13),
                      bg="white", fg="#1a237e", width=25,
                      command=command).pack(pady=8)
            
    # TODO: לתקן את הפאנל ואת הצבע
        
            # TODO: יצירת חשבון חדש
    def show_create_account(self):
        self.create_window = tk.Toplevel(self.root)
        self.create_window.title("Create Account")
        self.create_window.geometry("300x350")
        self.create_window.configure(bg="#1a237e")

        tk.Label(self.create_window, text="Create New Account",
                 font=("Segoe UI", 14, "bold"), bg="#1a237e", fg="white").pack(pady=10)
        
         # בעל חשבון חדש - שם חדש
        tk.Label(self.create_window, text="Name:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack(pady=3)
        self.new_name_entry = tk.Entry(self.create_window, font=("Segoe UI", 14),
                                       justify="center")
        self.new_name_entry.pack(pady=3)
   # PIN
        tk.Label(self.create_window, text="PIN (4 digits):", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack(pady=3)
        self.new_pin_entry = tk.Entry(self.create_window, font=("Segoe UI", 14),
                                      justify="center", show="*")
        self.new_pin_entry.pack(pady=3)
# balance
        tk.Label(self.create_window, text="Initial Balance:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack(pady=3)
        self.new_balance_entry = tk.Entry(self.create_window, font=("Segoe UI", 14),
                                          justify="center")
        self.new_balance_entry.pack(pady=3)
        
        tk.Button(self.create_window, text="Create", font=("Segoe UI", 13),
                  bg="#4caf50", fg="white", width=15,
                  command=self.do_create_account).pack(pady=15)
# כפתורים ללחיצת לוגיקה
    def do_create_account(self):
        name = self.new_name_entry.get()
        pin = self.new_pin_entry.get()
        balance_text = self.new_balance_entry.get()

        if name == "" or pin == "" or balance_text == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        if len(pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits")
            return
        try:
            balance = float(balance_text)
        except:
            messagebox.showerror("Error", "Balance must be a number")
            return
# יוצר מספר חשבון חדש - מוצא את הגבוה ביותר ומוסיף 1
        all_accounts = self.bank.accounts
        if len(all_accounts) == 0:
            new_number = "100"
        else:
            biggest = 0
            for num in all_accounts:
                if int(num) > biggest:
                    biggest = int(num)
            new_number = str(biggest + 1)

        success, message = self.bank.add_account(new_number, name, pin, balance)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", "Account created!\nAccount number: " + new_number)
        self.create_window.destroy()

# TODO: הצגה של חשבונות
# כל החשבנות
    def show_all_accounts(self):
        self.accounts_window = tk.Toplevel(self.root)
        self.accounts_window.title("all accounts")
        self.accounts_window.geometry("450x350")
        self.accounts_window.configure(bg="#1a237e")

        tk.Label(self.accounts_window, text="All Accounts",
                 font=("Segoe UI", 14, "bold"), bg="#1a237e", fg="white").pack(pady=10)

        # TODO: table with account info
        accounts_info = self.bank.get_all_accounts_info()

        if len(accounts_info) == 0:
            tk.Label(self.accounts_window, text="No accounts yet",
                     font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=20)
            return
        
                # הצגת חשבונות בתיבת טקסט
        text_box = tk.Text(self.accounts_window, font=("Segoe UI", 10),
                           width=50, height=15, state="normal")
        text_box.pack(pady=5)

        text_box.insert(tk.END, "Number | Name | Balance | Status\n")
        text_box.insert(tk.END, "-" * 40 + "\n")

        for acc in accounts_info:
            line = str(acc["number"]) + " | " + acc["name"] + " | " + str(acc["balance"]) + " | " + acc["status"]
            text_box.insert(tk.END, line + "\n")

        text_box.config(state="disabled")
        # TODO: חסימה ושחרור חשבון
    def show_toggle_account(self):
        self.toggle_window = tk.Toplevel(self.root)
        self.toggle_window.title("Block / Unblock")
        self.toggle_window.geometry("300x200")
        self.toggle_window.configure(bg="#1a237e")

        tk.Label(self.toggle_window, text="Enter account number:",
                 font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=10)

        self.toggle_entry = tk.Entry(self.toggle_window, font=("Segoe UI", 14),
                                     justify="center")
        self.toggle_entry.pack(pady=5)

        # TODO: button and logic



# ! תמיד למחוק TODO שנגמר ובוצע

    # -------- תפריט משתמש --------
    def show_user_menu(self):
        self.clear_screen()

        name = self.current_account.name
        balance = self.current_account.balance

        tk.Label(self.root, text="Welcome, " + name, font=("Segoe UI", 20, "bold"),
                 bg="#1a237e", fg="white").pack(pady=10)

        # שומרים reference כדי לעדכן את היתרה אחרי כל פעולה
        self.balance_label = tk.Label(self.root, text="Balance: " + str(balance),
                 font=("Segoe UI", 16), bg="#1a237e", fg="#4caf50")
        self.balance_label.pack(pady=5)

        # כל הכפתורים של התפריט
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

    # -------- הפקדה --------
    def show_deposit(self):
        # פותח חלון חדש להפקדה
        self.deposit_window = tk.Toplevel(self.root)
        self.deposit_window.title("Deposit")
        self.deposit_window.geometry("300x200")
        self.deposit_window.configure(bg="#1a237e")

        tk.Label(self.deposit_window, text="Enter amount:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=10)

        self.deposit_entry = tk.Entry(self.deposit_window, font=("Segoe UI", 14),
                                      justify="center")
        self.deposit_entry.pack(pady=5)

        tk.Button(self.deposit_window, text="Deposit", font=("Segoe UI", 13),
                  bg="#4caf50", fg="white", width=15,
                  command=self.do_deposit).pack(pady=15)

    # מבצע את ההפקדה בפועל אחרי לחיצה על הכפתור
    def do_deposit(self):
        text = self.deposit_entry.get()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount")
            return
        # בדיקה שהמשתמש הכניס מספר ולא טקסט
        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        success, message = self.current_account.deposit(amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        self.balance_label.config(text="Balance: " + str(self.current_account.balance))
        messagebox.showinfo("Success", message)
        self.deposit_window.destroy()

    # -------- משיכה --------
    # אותו עיקרון כמו הפקדה רק קורא ל-withdraw
    def show_withdraw(self):
        self.withdraw_window = tk.Toplevel(self.root)
        self.withdraw_window.title("Withdraw")
        self.withdraw_window.geometry("300x200")
        self.withdraw_window.configure(bg="#1a237e")

        tk.Label(self.withdraw_window, text="Enter amount:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=10)

        self.withdraw_entry = tk.Entry(self.withdraw_window, font=("Segoe UI", 14),
                                       justify="center")
        self.withdraw_entry.pack(pady=5)

        tk.Button(self.withdraw_window, text="Withdraw", font=("Segoe UI", 13),
                  bg="#f44336", fg="white", width=15,
                  command=self.do_withdraw).pack(pady=15)

    def do_withdraw(self):
        text = self.withdraw_entry.get()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount")
            return
        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        success, message = self.current_account.withdraw(amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        self.balance_label.config(text="Balance: " + str(self.current_account.balance))
        messagebox.showinfo("Success", message)
        self.withdraw_window.destroy()

    # -------- העברה --------
    # צריך שני שדות - מספר חשבון יעד וסכום
    def show_transfer(self):
        self.transfer_window = tk.Toplevel(self.root)
        self.transfer_window.title("Transfer")
        self.transfer_window.geometry("300x250")
        self.transfer_window.configure(bg="#1a237e")

        tk.Label(self.transfer_window, text="Target account number:",
                 font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=5)

        self.transfer_target_entry = tk.Entry(self.transfer_window,
                                              font=("Segoe UI", 14), justify="center")
        self.transfer_target_entry.pack(pady=5)

        tk.Label(self.transfer_window, text="Amount:",
                 font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=5)

        self.transfer_amount_entry = tk.Entry(self.transfer_window,
                                              font=("Segoe UI", 14), justify="center")
        self.transfer_amount_entry.pack(pady=5)

        tk.Button(self.transfer_window, text="Transfer", font=("Segoe UI", 13),
                  bg="#ff9800", fg="white", width=15,
                  command=self.do_transfer).pack(pady=15)

    def do_transfer(self):
        target = self.transfer_target_entry.get()
        text = self.transfer_amount_entry.get()

        if target == "" or text == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        # בדיקה שלא מעבירים לעצמך
        if target == self.current_account.account_number:
            messagebox.showerror("Error", "Cannot transfer to yourself")
            return
        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        # הלוגיקה של ההעברה נמצאת ב-Bank ולא כאן
        success, message = self.bank.transfer(self.current_account, target, amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        self.balance_label.config(text="Balance: " + str(self.current_account.balance))
        messagebox.showinfo("Success", message)
        self.transfer_window.destroy()

    # -------- היסטוריה --------
    # מציג את כל הפעולות שנעשו בחשבון
    def show_history(self):
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("Transaction History")
        self.history_window.geometry("400x350")
        self.history_window.configure(bg="#1a237e")

        tk.Label(self.history_window, text="Transaction History",
                 font=("Segoe UI", 16, "bold"), bg="#1a237e", fg="white").pack(pady=10)

        history = self.current_account.history

                # אם אין עסקאות עדיין
        if len(history) == 0:
            tk.Label(self.history_window, text="No transactions yet",
                     font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=20)
            return

        # תיבת טקסט להצגת העסקאות
        text_box = tk.Text(self.history_window, font=("Segoe UI", 10),
                           width=45, height=15, state="normal")
        text_box.pack(pady=5)

        # עובר על כל עסקה ומוסיף שורה
        for record in history:
            line = record["date"] + " | " + record["type"] + " | " + str(record["amount"])
            if "target" in record:
                line = line + " | account " + str(record["target"])
            text_box.insert(tk.END, line + "\n")

        # נועל את הטקסט שהמשתמש לא ישנה
        text_box.config(state="disabled")


    # -------- שינוי PIN --------
    def show_change_pin(self):
        self.pin_window = tk.Toplevel(self.root)
        self.pin_window.title("Change PIN")
        self.pin_window.geometry("300x300")
        self.pin_window.configure(bg="#1a237e")

        tk.Label(self.pin_window, text="Change PIN",
                 font=("Segoe UI", 16, "bold"), bg="#1a237e", fg="white").pack(pady=10)

        # PIN נוכחי
        tk.Label(self.pin_window, text="Current PIN:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack(pady=3)
        self.old_pin_entry = tk.Entry(self.pin_window, font=("Segoe UI", 14),
                                      justify="center", show="*")
        self.old_pin_entry.pack(pady=3)

        # PIN חדש
        tk.Label(self.pin_window, text="New PIN:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack(pady=3)
        self.new_pin_entry = tk.Entry(self.pin_window, font=("Segoe UI", 14),
                                      justify="center", show="*")
        self.new_pin_entry.pack(pady=3)

        # אימות PIN חדש
        tk.Label(self.pin_window, text="Confirm New PIN:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack(pady=3)
        self.confirm_pin_entry = tk.Entry(self.pin_window, font=("Segoe UI", 14),
                                          justify="center", show="*")
        self.confirm_pin_entry.pack(pady=3)

        tk.Button(self.pin_window, text="Change PIN", font=("Segoe UI", 13),
                  bg="#ff9800", fg="white", width=15,
                  command=self.do_change_pin).pack(pady=10)

    def do_change_pin(self):
        old = self.old_pin_entry.get()
        new = self.new_pin_entry.get()
        confirm = self.confirm_pin_entry.get()

        if old == "" or new == "" or confirm == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        # בדיקה שהPIN החדש והאימות תואמים
        if new != confirm:
            messagebox.showerror("Error", "New PIN does not match")
            return

        success, message = self.current_account.change_pin(old, new)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", message)
        self.pin_window.destroy()




