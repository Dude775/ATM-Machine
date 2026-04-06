import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONT_TITLE, FONT_SUBTITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON, FONT_TEXT

# פאנל מנהל
class AdminScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg=COLORS["bg"])
        self.app = app

        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Admin Panel", font=FONT_TITLE,
                 bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 5))

        tk.Frame(center, bg=COLORS["red"], height=3, width=200).pack(pady=(0, 25))

        buttons = [
            ("Create Account", self.show_create, COLORS["green"]),
            ("View All Accounts", self.show_all, COLORS["bg_light"]),
            ("Block / Unblock Account", self.show_toggle, COLORS["orange"]),
        ]

        for text, cmd, color in buttons:
            tk.Button(center, text=text, font=FONT_BUTTON,
                      bg=color, fg=COLORS["white"], width=25,
                      relief="flat", cursor="hand2",
                      command=cmd).pack(pady=5, ipady=3)

        tk.Button(center, text="Logout", font=("Segoe UI", 11),
                  bg=COLORS["bg"], fg=COLORS["red"], width=25,
                  relief="flat", cursor="hand2", bd=0,
                  command=lambda: self.app.show_screen("login")).pack(pady=(20, 0))

    # יצירת חשבון חדש - popup
    def show_create(self):
        self.create_win = tk.Toplevel(self.app.root)
        self.create_win.title("Create Account")
        self.create_win.geometry("350x380")
        self.create_win.configure(bg=COLORS["bg"])
        self.create_win.resizable(False, False)

        center = tk.Frame(self.create_win, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Create New Account",
                 font=FONT_SUBTITLE, bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 15))

        tk.Label(center, text="Name", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.name_entry = tk.Entry(center, font=FONT_ENTRY, justify="center",
                                   bg=COLORS["bg_light"], fg=COLORS["white"],
                                   insertbackground="white", relief="flat", width=20)
        self.name_entry.pack(pady=(3, 10), ipady=4)

        tk.Label(center, text="PIN (4 digits)", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.pin_entry = tk.Entry(center, font=FONT_ENTRY, justify="center", show="*",
                                  bg=COLORS["bg_light"], fg=COLORS["white"],
                                  insertbackground="white", relief="flat", width=20)
        self.pin_entry.pack(pady=(3, 10), ipady=4)

        tk.Label(center, text="Initial Balance", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.balance_entry = tk.Entry(center, font=FONT_ENTRY, justify="center",
                                      bg=COLORS["bg_light"], fg=COLORS["white"],
                                      insertbackground="white", relief="flat", width=20)
        self.balance_entry.pack(pady=(3, 15), ipady=4)

        tk.Button(center, text="Create", font=FONT_BUTTON,
                  bg=COLORS["green"], fg=COLORS["white"], width=18,
                  relief="flat", cursor="hand2",
                  command=self.do_create).pack(ipady=3)

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

    # הצגת כל החשבונות
    def show_all(self):
        self.all_win = tk.Toplevel(self.app.root)
        self.all_win.title("all accounts")
        self.all_win.geometry("480x380")
        self.all_win.configure(bg=COLORS["bg"])

        center = tk.Frame(self.all_win, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="All Accounts",
                 font=FONT_SUBTITLE, bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 10))

        accounts = self.app.bank.get_all_accounts_info()

        if len(accounts) == 0:
            tk.Label(center, text="no accounts yet",
                     font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["text_light"]).pack(pady=20)
            return

        text_box = tk.Text(center, font=FONT_TEXT, width=50, height=15,
                           bg=COLORS["bg_light"], fg=COLORS["white"], relief="flat")
        text_box.pack(pady=5)

        text_box.insert(tk.END, "  Number | Name      | Balance    | Status\n")
        text_box.insert(tk.END, "  " + "-" * 44 + "\n")

        for acc in accounts:
            line = "  " + str(acc["number"]) + "    | " + acc["name"] + "     | " + str(acc["balance"]) + "    | " + acc["status"]
            text_box.insert(tk.END, line + "\n")

        text_box.config(state="disabled")

    # חסימה / שחרור חשבון
    def show_toggle(self):
        self.toggle_win = tk.Toplevel(self.app.root)
        self.toggle_win.title("Block / Unblock")
        self.toggle_win.geometry("320x220")
        self.toggle_win.configure(bg=COLORS["bg"])
        self.toggle_win.resizable(False, False)

        center = tk.Frame(self.toggle_win, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Enter account number",
                 font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["text_light"]).pack(pady=(0, 5))

        self.toggle_entry = tk.Entry(center, font=FONT_ENTRY, justify="center",
                                     bg=COLORS["bg_light"], fg=COLORS["white"],
                                     insertbackground="white", relief="flat", width=20)
        self.toggle_entry.pack(pady=(3, 20), ipady=5)

        tk.Button(center, text="Toggle Status", font=FONT_BUTTON,
                  bg=COLORS["orange"], fg=COLORS["white"], width=18,
                  relief="flat", cursor="hand2",
                  command=self.do_toggle).pack(ipady=3)

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
