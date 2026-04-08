import tkinter as tk
import os
from datetime import datetime
from tkinter import messagebox
from storage import save_data


class ATMApp:
    COLORS = {
        "bg": "#1a1a2e",
        "card": "#16213e",
        "accent": "#0f3460",
        "btn_bg": "#0f3460",
        "btn_fg": "#e8e8e8",
        "btn_hover": "#1a5276",
        "text": "#ffffff",
        "text2": "#a8b2d1",
        "entry_bg": "#1c2541",
        "entry_fg": "#ffffff",
        "success": "#2ecc71",
        "danger": "#e74c3c",
    }

    def __init__(self, root, bank):
        self.root = root
        self.bank = bank
        self.current_account = None  # מי שמחובר עכשיו - בהתחלה אף אחד

        self.root.title("ATM Machine")
        self.root.geometry("800x600")
        self.root.configure(bg=self.COLORS["bg"])
        self.root.resizable(True, True)
        self.root.minsize(400, 550)

        # clock label - stays on screen always
        self.clock_label = tk.Label(self.root, font=("Segoe UI", 10),
                                    bg=self.COLORS["bg"], fg=self.COLORS["text2"])
        self.clock_label.place(x=10, y=10)
        self.update_clock()

        # מסך ראשון שנטען כשפותחים את התוכנה
        self.show_login_screen()

    def update_clock(self):
        now = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    # מוחק את כל מה שעל המסך - משתמשים בזה לפני כל מעבר מסך
    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget != self.clock_label:
                widget.destroy()

    def _center_frame(self):
        container = tk.Frame(self.root, bg=self.COLORS["bg"])
        container.place(relx=0.5, rely=0.5, anchor="center")
        return container

    def _btn_style(self):
        return {
            "font": ("Segoe UI", 12, "bold"),
            "bg": self.COLORS["btn_bg"],
            "fg": self.COLORS["btn_fg"],
            "activebackground": self.COLORS["btn_hover"],
            "activeforeground": self.COLORS["btn_fg"],
            "relief": "flat",
            "cursor": "hand2",
            "width": 20,
            "pady": 8,
        }

    def _small_btn_style(self):
        return {
            "font": ("Segoe UI", 9, "bold"),
            "bg": self.COLORS["btn_bg"],
            "fg": self.COLORS["btn_fg"],
            "activebackground": self.COLORS["btn_hover"],
            "activeforeground": self.COLORS["btn_fg"],
            "relief": "flat",
            "cursor": "hand2",
            "pady": 3,
            "padx": 6,
        }

    def _entry_style(self):
        return {
            "font": ("Segoe UI", 13),
            "bg": self.COLORS["entry_bg"],
            "fg": self.COLORS["entry_fg"],
            "insertbackground": self.COLORS["entry_fg"],
            "relief": "flat",
            "justify": "center",
            "highlightthickness": 1,
            "highlightbackground": self.COLORS["accent"],
            "highlightcolor": self.COLORS["success"],
        }

    def _back_btn(self, parent, command):
        back_style = self._btn_style()
        back_style["bg"] = self.COLORS["danger"]
        back_style["activebackground"] = "#c0392b"
        tk.Button(parent, text="Back", command=command,
                  **back_style).pack(pady=(10, 0))

    # -------- מסך כניסה --------
    def show_login_screen(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])
        self.current_account = None  # מנקה את המשתמש המחובר

        frame = self._center_frame()

        tk.Label(frame, text="ATM Machine", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 25))

        tk.Label(frame, text="Account Number:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))
        self.acc_entry = tk.Entry(frame, **self._entry_style())
        self.acc_entry.pack(pady=(0, 10))

        # שדה PIN - מוסתר עם כוכביות
        tk.Label(frame, text="PIN:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))
        self.pin_entry = tk.Entry(frame, show="*", **self._entry_style())
        self.pin_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Login", command=self.handle_login,
                  **self._btn_style()).pack(pady=5)

        # כפתור admin באדום
        admin_style = self._btn_style()
        admin_style["bg"] = self.COLORS["danger"]
        admin_style["activebackground"] = "#c0392b"
        tk.Button(frame, text="Admin", command=self.handle_admin_login,
                  **admin_style).pack(pady=5)

    # בודק את הפרטים שהוזנו ומחליט אם להכניס או לא
    def handle_login(self):
        acc_number = self.acc_entry.get()
        pin = self.pin_entry.get()

        # NOTE: סדר הבדיקות חשוב - קודם בודקים אם קיים, אחכ אם חסום, אחכ PIN
        account = self.bank.get_account(acc_number)
        if account is None:
            messagebox.showerror("Error", "Account not found")
            return
        if not account.is_active():
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
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Admin Login", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        tk.Label(frame, text="Admin Password:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.admin_pass_entry = tk.Entry(frame, show="*", **self._entry_style())
        self.admin_pass_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Login", command=self.check_admin_password,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_login_screen)

    # בודק אם הסיסמה נכונה
    def check_admin_password(self):
        password = self.admin_pass_entry.get()
        if password == self.bank.admin_password:
            self.show_admin_menu()
        else:
            messagebox.showerror("Error", "Wrong admin password")
# !  מפה זה כל החלק של תפריט מנהל - UI/UX
    # -------- תפריט מנהל --------
    def show_admin_menu(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Admin Panel", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        buttons = [
            ("Create Account", self.show_create_account),
            ("View All Accounts", self.show_all_accounts),
            ("Block / Unblock Account", self.show_toggle_account),
            ("Search Account", self.show_search_account),
            ("System Stats", self.show_system_stats),
        ]

        for text, command in buttons:
            tk.Button(frame, text=text, command=command,
                      **self._btn_style()).pack(pady=5)

        # logout button
        logout_style = self._btn_style()
        logout_style["bg"] = self.COLORS["danger"]
        logout_style["activebackground"] = "#c0392b"
        tk.Button(frame, text="Logout", command=self.show_login_screen,
                  **logout_style).pack(pady=(15, 0))

    def show_create_account(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Create New Account", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 15))

         # בעל חשבון חדש - שם חדש
        tk.Label(frame, text="Name:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(3, 1))
        self.new_name_entry = tk.Entry(frame, **self._entry_style())
        self.new_name_entry.pack(pady=(0, 5))

        tk.Label(frame, text="ID Number (9 digits):", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(3, 1))
        self.new_id_entry = tk.Entry(frame, **self._entry_style())
        self.new_id_entry.pack(pady=(0, 5))
   # PIN
        tk.Label(frame, text="PIN (4 digits):", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(3, 1))
        self.new_pin_entry = tk.Entry(frame, show="*", **self._entry_style())
        self.new_pin_entry.pack(pady=(0, 5))

        tk.Label(frame, text="Email:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(3, 1))
        self.new_email_entry = tk.Entry(frame, **self._entry_style())
        self.new_email_entry.pack(pady=(0, 5))

        tk.Label(frame, text="Address (optional):", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(3, 1))
        self.new_address_entry = tk.Entry(frame, **self._entry_style())
        self.new_address_entry.pack(pady=(0, 5))
# balance
        tk.Label(frame, text="Initial Balance:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(3, 1))
        self.new_balance_entry = tk.Entry(frame, **self._entry_style())
        self.new_balance_entry.pack(pady=(0, 10))

        tk.Button(frame, text="Create", command=self.do_create_account,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_admin_menu)

# כפתורים ללחיצת לוגיקה
    def do_create_account(self):
        name = self.new_name_entry.get()
        id_number = self.new_id_entry.get()
        pin = self.new_pin_entry.get()
        email = self.new_email_entry.get()
        address = self.new_address_entry.get()
        balance_text = self.new_balance_entry.get()

        if name == "" or pin == "" or balance_text == "" or id_number == "" or email == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        if len(name) < 2:
            messagebox.showerror("Error", "Name must be at least 2 characters")
            return
        if len(id_number) != 9 or not id_number.isdigit():
            messagebox.showerror("Error", "ID must be exactly 9 digits")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email")
            return
        if len(pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits")
            return
        try:
            balance = float(balance_text)
        except ValueError:
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

        success, message = self.bank.add_account(new_number, name, pin, balance,
                                                  email=email, id_number=id_number,
                                                  address=address)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", "Account created!\nAccount number: " + new_number)
        self.show_admin_menu()

# כל החשבנות
    def show_all_accounts(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        # title at top
        tk.Label(self.root, text="All Accounts", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(40, 10))

        accounts_info = self.bank.get_all_accounts_info()

        if len(accounts_info) == 0:
            tk.Label(self.root, text="No accounts yet", font=("Segoe UI", 12),
                     bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=20)
        else:
            #print("got here")
            list_frame = tk.Frame(self.root, bg=self.COLORS["bg"])
            list_frame.pack(pady=5)


            canvas = tk.Canvas(list_frame, bg=self.COLORS["bg"], highlightthickness=0)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas, bg=self.COLORS["bg"])

            scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", padx=(0, 15)) 
            scroll_frame.configure(padx=10)         


            canvas.pack(side="left")
            scrollbar.pack(side="right", fill="y")

            for acc in accounts_info:
                row = tk.Frame(scroll_frame, bg=self.COLORS["card"], pady=8, padx=10)
                row.pack(anchor="center", pady=3)


                # account info
                status_color = self.COLORS["success"] if acc["status"] == "active" else self.COLORS["danger"]
                status_text = "Active" if acc["status"] == "active" else "Blocked"

                info_text = "#" + str(acc["number"]) + "  |  " + acc["name"] + "  |  " + "{:,.2f}".format(acc["balance"]) + "  |  "
                tk.Label(row, text=info_text, font=("Consolas", 10),
                         bg=self.COLORS["card"], fg=self.COLORS["text"]).pack(side="left")
                tk.Label(row, text=status_text, font=("Consolas", 10, "bold"),
                         bg=self.COLORS["card"], fg=status_color).pack(side="left")

                # buttons
                acc_number = acc["number"]
                btn_frame = tk.Frame(row, bg=self.COLORS["card"])
                btn_frame.pack(side="right")

                tk.Button(btn_frame, text="Details",
                          command=lambda n=acc_number: self.show_account_details(n),
                          **self._small_btn_style()).pack(side="left", padx=2)
                tk.Button(btn_frame, text="History",
                          command=lambda n=acc_number: self.show_account_history(
                              self.bank.get_account(n), self.show_all_accounts),
                          **self._small_btn_style()).pack(side="left", padx=2)

                toggle_btn_style = self._small_btn_style()
                toggle_btn_style["bg"] = self.COLORS["danger"]
                toggle_btn_style["activebackground"] = "#c0392b"
                tk.Button(btn_frame, text="Toggle",
                          command=lambda n=acc_number: self._toggle_from_list(n),
                          **toggle_btn_style).pack(side="left", padx=2)

        self._back_btn(self.root, self.show_admin_menu)

    def _toggle_from_list(self, acc_number):
        success, message = self.bank.toggle_account(acc_number)
        if not success:
            messagebox.showerror("Error", message)
            return
        save_data(self.bank)
        messagebox.showinfo("Success", message)
        self.show_all_accounts()

    def show_account_history(self, account, return_to):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        title = "History — Account #" + account.account_number + " (" + account.name + ")"
        tk.Label(frame, text=title, font=("Segoe UI", 16, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 15))

        history = account.history

        if len(history) == 0:
            tk.Label(frame, text="No transactions yet", font=("Segoe UI", 12),
                     bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=20)
        else:
            text_box = tk.Text(frame, font=("Consolas", 10),
                               bg=self.COLORS["card"], fg=self.COLORS["text"],
                               width=55, height=15, state="normal",
                               relief="flat", highlightthickness=1,
                               highlightbackground=self.COLORS["accent"])
            text_box.pack(pady=5)

            text_box.tag_config("deposit", foreground=self.COLORS["success"])
            text_box.tag_config("withdraw", foreground=self.COLORS["danger"])
            text_box.tag_config("transfer_out", foreground=self.COLORS["danger"])
            text_box.tag_config("transfer_in", foreground=self.COLORS["success"])
            text_box.tag_config("header", foreground=self.COLORS["text2"],
                                font=("Consolas", 10, "bold"))

            text_box.insert(tk.END, "  Date            | Type         | Amount    | Balance\n", "header")
            text_box.insert(tk.END, "  " + "-" * 54 + "\n", "header")

            for record in history:
                r_type = record["type"]
                if r_type in ("deposit", "transfer_in"):
                    sign = "+"
                else:
                    sign = "-"

                line = "  " + record["date"] + "  |  " + r_type
                line = line + "  |  " + sign + str(record["amount"])
                if "balance_after" in record:
                    line = line + "  |  " + str(record["balance_after"])
                if "target" in record:
                    line = line + "  -> #" + str(record["target"])
                text_box.insert(tk.END, line + "\n", r_type)

            text_box.config(state="disabled")

        self._back_btn(frame, return_to)

    def show_account_details(self, acc_number):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        account = self.bank.get_account(acc_number)
        if account is None:
            messagebox.showerror("Error", "Account not found")
            self.show_all_accounts()
            return

        frame = self._center_frame()

        tk.Label(frame, text="Account Details", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        status_color = self.COLORS["success"] if account.is_active() else self.COLORS["danger"]
        status_text = "Active" if account.is_active() else "Blocked"

        first_date = "No transactions yet"
        if len(account.history) > 0:
            first_date = account.history[0]["date"]

        details = [
            ("Account Number", account.account_number),
            ("Name", account.name),
            ("ID Number", account.id_number if account.id_number else "N/A"),
            ("Email", account.email if account.email else "N/A"),
            ("Address", account.address if account.address else "N/A"),
            ("Balance", "{:,.2f}".format(account.balance) + " ₪"),
            ("Total Transactions", str(len(account.history))),
            ("First Transaction", first_date),
        ]

        for label, value in details:
            row = tk.Frame(frame, bg=self.COLORS["bg"])
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label + ":", font=("Segoe UI", 11, "bold"),
                     bg=self.COLORS["bg"], fg=self.COLORS["text2"],
                     width=18, anchor="e").pack(side="left")
            tk.Label(row, text="  " + value, font=("Segoe UI", 11),
                     bg=self.COLORS["bg"], fg=self.COLORS["text"],
                     anchor="w").pack(side="left")

        # status row with color
        row = tk.Frame(frame, bg=self.COLORS["bg"])
        row.pack(fill="x", pady=2)
        tk.Label(row, text="Status:", font=("Segoe UI", 11, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"],
                 width=18, anchor="e").pack(side="left")
        tk.Label(row, text="  " + status_text, font=("Segoe UI", 11, "bold"),
                 bg=self.COLORS["bg"], fg=status_color,
                 anchor="w").pack(side="left")

        self._back_btn(frame, self.show_all_accounts)

    def show_toggle_account(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Block / Unblock", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        tk.Label(frame, text="Enter account number:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.toggle_entry = tk.Entry(frame, **self._entry_style())
        self.toggle_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Toggle", command=self.do_toggle_account,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_admin_menu)

    def do_toggle_account(self):
        acc_number = self.toggle_entry.get()
        if acc_number == "":
            messagebox.showerror("Error", "Please enter account number")
            return

        success, message = self.bank.toggle_account(acc_number)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", message)
        self.show_admin_menu()

    # -------- search account --------
    def show_search_account(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Search Account", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        tk.Label(frame, text="Account number or name:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.search_entry = tk.Entry(frame, **self._entry_style())
        self.search_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Search", command=self.do_search_account,
                  **self._btn_style()).pack(pady=5)

        # result area
        self.search_result_frame = tk.Frame(frame, bg=self.COLORS["bg"])
        self.search_result_frame.pack(pady=10)

        self._back_btn(frame, self.show_admin_menu)

    def do_search_account(self):
        query = self.search_entry.get()
        if query == "":
            messagebox.showerror("Error", "Please enter search query")
            return

        # clear previous results
        for widget in self.search_result_frame.winfo_children():
            widget.destroy()

        account = self.bank.search_account(query)
        if account is None:
            tk.Label(self.search_result_frame, text="Account not found",
                     font=("Segoe UI", 12), bg=self.COLORS["bg"],
                     fg=self.COLORS["danger"]).pack(pady=10)
            return

        # show result
        status_color = self.COLORS["success"] if account.is_active() else self.COLORS["danger"]
        status_text = "Active" if account.is_active() else "Blocked"

        info_lines = [
            "#" + account.account_number + "  |  " + account.name,
            "Balance: " + "{:,.2f}".format(account.balance) + " ₪",
            "ID: " + (account.id_number if account.id_number else "N/A"),
            "Email: " + (account.email if account.email else "N/A"),
            "Status: " + status_text,
        ]
        for line in info_lines:
            tk.Label(self.search_result_frame, text=line, font=("Segoe UI", 11),
                     bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=1)

        btn_row = tk.Frame(self.search_result_frame, bg=self.COLORS["bg"])
        btn_row.pack(pady=8)

        acc_num = account.account_number
        tk.Button(btn_row, text="Details",
                  command=lambda: self.show_account_details(acc_num),
                  **self._small_btn_style()).pack(side="left", padx=5)
        tk.Button(btn_row, text="History",
                  command=lambda: self.show_account_history(account, self.show_search_account),
                  **self._small_btn_style()).pack(side="left", padx=5)

    # admin stats - i think this is cool
    def show_system_stats(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="System Stats", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 25))

        stats = self.bank.get_system_stats()

        stat_lines = [
            ("Total Accounts", str(stats["total_accounts"])),
            ("Active Accounts", str(stats["active"])),
            ("blocked accounts", str(stats["blocked"])),
            ("Total Transactions", str(stats["total_transactions"])),
            ("Total Balance", "{:,.2f} ₪".format(stats["total_balance"])),
        ]

        for label, value in stat_lines:
            row = tk.Frame(frame, bg=self.COLORS["bg"])
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label + ":", font=("Segoe UI", 13, "bold"),
                     bg=self.COLORS["bg"], fg=self.COLORS["text2"],
                     width=20, anchor="e").pack(side="left")
            tk.Label(row, text="  " + value, font=("Segoe UI", 13),
                     bg=self.COLORS["bg"], fg=self.COLORS["success"],
                     anchor="w").pack(side="left")

        self._back_btn(frame, self.show_admin_menu)

    # -------- תפריט משתמש --------
    def show_user_menu(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        name = self.current_account.name
        balance = self.current_account.balance

        frame = self._center_frame()

        tk.Label(frame, text="Welcome, " + name, font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 5))

        tk.Label(frame, text="Account #" + self.current_account.account_number,
                 font=("Segoe UI", 10), bg=self.COLORS["bg"],
                 fg=self.COLORS["text2"]).pack(pady=(0, 10))

        # שומרים reference כדי לעדכן את היתרה אחרי כל פעולה
        self.balance_label = tk.Label(frame, text="{:,.2f} ₪".format(balance),
                 font=("Segoe UI", 28, "bold"), bg=self.COLORS["bg"],
                 fg=self.COLORS["success"])
        self.balance_label.pack(pady=(0, 20))

        # כל הכפתורים של התפריט
        buttons = [
            ("Deposit", self.show_deposit),
            ("Withdraw", self.show_withdraw),
            ("Transfer", self.show_transfer),
            ("History", self.show_history),
            ("Change PIN", self.show_change_pin),
        ]

        for text, command in buttons:
            tk.Button(frame, text=text, command=command,
                      **self._btn_style()).pack(pady=4)

        logout_style = self._btn_style()
        logout_style["bg"] = self.COLORS["danger"]
        logout_style["activebackground"] = "#c0392b"
        tk.Button(frame, text="Logout", command=self.show_login_screen,
                  **logout_style).pack(pady=(12, 0))

    # -------- הפקדה --------
    def show_deposit(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Deposit", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        tk.Label(frame, text="Enter amount:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.deposit_entry = tk.Entry(frame, **self._entry_style())
        self.deposit_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Deposit", command=self.do_deposit,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_user_menu)

    # מבצע את ההפקדה בפועל אחרי לחיצה על הכפתור
    def do_deposit(self):
        text = self.deposit_entry.get()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount")
            return
        try:
            amount = float(text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        success, message = self.current_account.deposit(amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", message)
        self.show_user_menu()

    # -------- משיכה --------
    # אותו עיקרון כמו הפקדה רק קורא ל-withdraw
    def show_withdraw(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Withdraw", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        tk.Label(frame, text="Enter amount:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.withdraw_entry = tk.Entry(frame, **self._entry_style())
        self.withdraw_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Withdraw", command=self.do_withdraw,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_user_menu)

    def do_withdraw(self):
        text = self.withdraw_entry.get()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount")
            return
        try:
            amount = float(text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        success, message = self.current_account.withdraw(amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", message)
        self.show_user_menu()

    # -------- העברה --------
    # צריך שני שדות - מספר חשבון יעד וסכום
    def show_transfer(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Transfer", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        tk.Label(frame, text="Target account number:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.transfer_target_entry = tk.Entry(frame, **self._entry_style())
        self.transfer_target_entry.pack(pady=(0, 10))

        tk.Label(frame, text="Amount:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))

        self.transfer_amount_entry = tk.Entry(frame, **self._entry_style())
        self.transfer_amount_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Transfer", command=self.do_transfer,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_user_menu)

    def do_transfer(self):
        tgt = self.transfer_target_entry.get()
        text = self.transfer_amount_entry.get()

        if tgt == "" or text == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        # בדיקה שלא מעבירים לעצמך
        if tgt == self.current_account.account_number:
            messagebox.showerror("Error", "Cannot transfer to yourself")
            return
        try:
            amount = float(text)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        # הלוגיקה של ההעברה נמצאת ב-Bank ולא כאן
        success, message = self.bank.transfer(self.current_account, tgt, amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        save_data(self.bank)
        messagebox.showinfo("Success", message)
        self.show_user_menu()

    # -------- היסטוריה --------
    # מציג את כל הפעולות שנעשו בחשבון
    def show_history(self):
        self.show_account_history(self.current_account, self.show_user_menu)

    # -------- שינוי PIN --------
    def show_change_pin(self):
        self.clear_screen()
        self.root.configure(bg=self.COLORS["bg"])

        frame = self._center_frame()

        tk.Label(frame, text="Change PIN", font=("Segoe UI", 22, "bold"),
                 bg=self.COLORS["bg"], fg=self.COLORS["text"]).pack(pady=(0, 20))

        # PIN נוכחי
        tk.Label(frame, text="Current PIN:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))
        self.old_pin_entry = tk.Entry(frame, show="*", **self._entry_style())
        self.old_pin_entry.pack(pady=(0, 8))

        # PIN חדש
        tk.Label(frame, text="New PIN:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))
        self.new_pin_entry = tk.Entry(frame, show="*", **self._entry_style())
        self.new_pin_entry.pack(pady=(0, 8))

        # אימות PIN חדש
        tk.Label(frame, text="Confirm New PIN:", font=("Segoe UI", 11),
                 bg=self.COLORS["bg"], fg=self.COLORS["text2"]).pack(pady=(5, 2))
        self.confirm_pin_entry = tk.Entry(frame, show="*", **self._entry_style())
        self.confirm_pin_entry.pack(pady=(0, 15))

        tk.Button(frame, text="Change PIN", command=self.do_change_pin,
                  **self._btn_style()).pack(pady=5)

        self._back_btn(frame, self.show_user_menu)

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
        self.show_user_menu()
