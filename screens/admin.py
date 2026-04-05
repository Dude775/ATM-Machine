import tkinter as tk
from tkinter import messagebox

# פאנל מנהל
class AdminScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg="#1a237e")
        self.app = app

        tk.Label(self, text="Admin Panel", font=("Segoe UI", 22, "bold"),
                 bg="#1a237e", fg="white").pack(pady=15)

        tk.Button(self, text="Create Account", font=("Segoe UI", 13),
                  bg="white", fg="#1a237e", width=25,
                  command=self.show_create).pack(pady=8)

        tk.Button(self, text="View All Accounts", font=("Segoe UI", 13),
                  bg="white", fg="#1a237e", width=25,
                  command=self.show_all).pack(pady=8)

        tk.Button(self, text="Block / Unblock Account", font=("Segoe UI", 13),
                  bg="white", fg="#1a237e", width=25,
                  command=self.show_toggle).pack(pady=8)

        tk.Button(self, text="Logout", font=("Segoe UI", 13),
                  bg="#f44336", fg="white", width=25,
                  command=lambda: self.app.show_screen("login")).pack(pady=8)

    def show_create(self):
        self.create_win = tk.Toplevel(self.app.root)
        self.create_win.title("Create Account")
        self.create_win.geometry("300x350")
        self.create_win.configure(bg="#1a237e")

        tk.Label(self.create_win, text="Create New Account",
                 font=("Segoe UI", 14, "bold"), bg="#1a237e", fg="white").pack(pady=10)

        tk.Label(self.create_win, text="Name:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack()
        self.name_entry = tk.Entry(self.create_win, font=("Segoe UI", 13), justify="center")
        self.name_entry.pack(pady=3)

        tk.Label(self.create_win, text="PIN (4 digits):", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack()
        self.pin_entry = tk.Entry(self.create_win, font=("Segoe UI", 13),
                                  justify="center", show="*")
        self.pin_entry.pack(pady=3)

        tk.Label(self.create_win, text="Initial Balance:", font=("Segoe UI", 11),
                 bg="#1a237e", fg="white").pack()
        self.balance_entry = tk.Entry(self.create_win, font=("Segoe UI", 13), justify="center")
        self.balance_entry.pack(pady=3)

        tk.Button(self.create_win, text="Create", font=("Segoe UI", 13),
                  bg="#4caf50", fg="white", width=15,
                  command=self.do_create).pack(pady=15)

    def do_create(self):
        name = self.name_entry.get()
        pin = self.pin_entry.get()
        bal = self.balance_entry.get()

        if name == "" or pin == "" or bal == "":
            messagebox.showerror("Error", "fill all fields")
            return
        if len(pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits")
            return
        try:
            balance = float(bal)
        except:
            messagebox.showerror("Error", "balance must be a number")
            return

        all_acc = self.app.bank.accounts
        if len(all_acc) == 0:
            new_num = "100"
        else:
            biggest = 0
            for num in all_acc:
                if int(num) > biggest:
                    biggest = int(num)
            new_num = str(biggest + 1)

        success, msg = self.app.bank.add_account(new_num, name, pin, balance)
        if not success:
            messagebox.showerror("Error", msg)
            return

        self.app.save()
        messagebox.showinfo("Success", "Account created!\nnumber: " + new_num)
        self.create_win.destroy()

    # הצגת כל החשבונות במערכת
    def show_all(self):
        self.all_win = tk.Toplevel(self.app.root)
        self.all_win.title("all accounts")
        self.all_win.geometry("450x350")
        self.all_win.configure(bg="#1a237e")

        tk.Label(self.all_win, text="All Accounts",
                 font=("Segoe UI", 14, "bold"), bg="#1a237e", fg="white").pack(pady=10)

        accounts = self.app.bank.get_all_accounts_info()

        if len(accounts) == 0:
            tk.Label(self.all_win, text="no accounts yet",
                     font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=20)
            return

        text_box = tk.Text(self.all_win, font=("Segoe UI", 10), width=50, height=15)
        text_box.pack(pady=5)

        text_box.insert(tk.END, "Number | Name | Balance | Status\n")
        text_box.insert(tk.END, "-" * 40 + "\n")

        for acc in accounts:
            line = str(acc["number"]) + " | " + acc["name"] + " | " + str(acc["balance"]) + " | " + acc["status"]
            text_box.insert(tk.END, line + "\n")

        text_box.config(state="disabled")

    # TODO: block/unblock
    def show_toggle(self):
        self.toggle_win = tk.Toplevel(self.app.root)
        self.toggle_win.title("Block / Unblock")
        self.toggle_win.geometry("300x200")
        self.toggle_win.configure(bg="#1a237e")

        tk.Label(self.toggle_win, text="Enter account number:",
                 font=("Segoe UI", 12), bg="#1a237e", fg="white").pack(pady=10)

        self.toggle_entry = tk.Entry(self.toggle_win, font=("Segoe UI", 14),
                                     justify="center")
        self.toggle_entry.pack(pady=5)

        tk.Button(self.toggle_win, text="Toggle", font=("Segoe UI", 13),
                  bg="#f44336", fg="white", width=15,
                  command=self.do_toggle).pack(pady=15)

    def do_toggle(self):
        acc_num = self.toggle_entry.get()
        if acc_num == "":
            messagebox.showerror("Error", "Please enter account number")
            return

        success, msg = self.app.bank.toggle_account(acc_num)
        if not success:
            messagebox.showerror("Error", msg)
            return

        self.app.save()
        messagebox.showinfo("Success", msg)
        self.toggle_win.destroy()

