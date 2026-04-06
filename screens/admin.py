import customtkinter as ctk
from tkinter import messagebox

# פאנל מנהל - ניהול כל החשבונות
class AdminScreen(ctk.CTkFrame):
    def __init__(self, root, app):
        super().__init__(root, fg_color="#0A0E27", corner_radius=0)
        self.app = app

        ctk.CTkLabel(self, text="Admin Panel", font=("Inter", 22, "bold"),
                     text_color="white").pack(pady=(15, 4))

        # סטטיסטיקות למעלה
        stats_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=10)
        stats_frame.pack(padx=20, pady=8, fill="x")

        accounts_info = self.app.bank.get_all_accounts_info()
        total_accounts = len(accounts_info)
        total_balance = 0
        blocked_count = 0
        for acc in accounts_info:
            total_balance = total_balance + acc["balance"]
            if acc["status"] == "blocked":
                blocked_count = blocked_count + 1

        stats_inner = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_inner.pack(pady=10)

        # שלושה מספרים בשורה
        self.make_stat(stats_inner, "Accounts", str(total_accounts), "#3B82F6", 0)
        self.make_stat(stats_inner, "Total $", str(int(total_balance)), "#10B981", 1)
        self.make_stat(stats_inner, "Blocked", str(blocked_count), "#EF4444", 2)

        # טבלת חשבונות
        table_frame = ctk.CTkScrollableFrame(self, fg_color="#111827",
                                              corner_radius=10, height=200)
        table_frame.pack(padx=20, pady=5, fill="both", expand=True)

        # כותרת טבלה
        hdr = ctk.CTkFrame(table_frame, fg_color="#1F2937", corner_radius=6)
        hdr.pack(fill="x", pady=(0, 4))
        ctk.CTkLabel(hdr, text="#", font=("Inter", 10, "bold"),
                     text_color="#9CA3AF", width=50).pack(side="left", padx=4)
        ctk.CTkLabel(hdr, text="Name", font=("Inter", 10, "bold"),
                     text_color="#9CA3AF", width=80).pack(side="left", padx=4)
        ctk.CTkLabel(hdr, text="Balance", font=("Inter", 10, "bold"),
                     text_color="#9CA3AF", width=80).pack(side="left", padx=4)
        ctk.CTkLabel(hdr, text="Status", font=("Inter", 10, "bold"),
                     text_color="#9CA3AF", width=70).pack(side="left", padx=4)
        ctk.CTkLabel(hdr, text="Actions", font=("Inter", 10, "bold"),
                     text_color="#9CA3AF", width=120).pack(side="left", padx=4)

        # שורות חשבונות
        if total_accounts == 0:
            ctk.CTkLabel(table_frame, text="No accounts yet",
                         font=("Inter", 12), text_color="#6B7280").pack(pady=20)
        else:
            for acc in accounts_info:
                row = ctk.CTkFrame(table_frame, fg_color="#0A0E27", corner_radius=4)
                row.pack(fill="x", pady=1)

                ctk.CTkLabel(row, text=acc["number"], font=("Inter", 10),
                             text_color="white", width=50).pack(side="left", padx=4)
                ctk.CTkLabel(row, text=acc["name"], font=("Inter", 10),
                             text_color="white", width=80).pack(side="left", padx=4)
                ctk.CTkLabel(row, text="₪" + str(acc["balance"]),
                             font=("Inter", 10),
                             text_color="#10B981", width=80).pack(side="left", padx=4)

                # סטטוס עם צבע
                status_color = "#10B981" if acc["status"] == "active" else "#EF4444"
                ctk.CTkLabel(row, text=acc["status"], font=("Inter", 10),
                             text_color=status_color, width=70).pack(side="left", padx=4)

                # כפתורי פעולה
                btn_frame = ctk.CTkFrame(row, fg_color="transparent")
                btn_frame.pack(side="left", padx=4)

                # כפתור חסימה/שחרור
                toggle_text = "Block" if acc["status"] == "active" else "Unblock"
                toggle_color = "#EF4444" if acc["status"] == "active" else "#10B981"
                ctk.CTkButton(btn_frame, text=toggle_text, font=("Inter", 9),
                              fg_color=toggle_color, width=55, height=24, corner_radius=6,
                              command=lambda n=acc["number"]: self.do_toggle(n)).pack(side="left", padx=2)

                # כפתור היסטוריה
                ctk.CTkButton(btn_frame, text="History", font=("Inter", 9),
                              fg_color="#374151", width=55, height=24, corner_radius=6,
                              command=lambda n=acc["number"]: self.show_account_history(n)).pack(side="left", padx=2)

        # כפתורים למטה
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(pady=8)

        ctk.CTkButton(bottom, text="+ Create Account", font=("Inter", 12),
                      fg_color="#3B82F6", hover_color="#2563EB",
                      height=36, corner_radius=10, width=150,
                      command=self.show_create).pack(side="left", padx=5)

        ctk.CTkButton(bottom, text="Logout", font=("Inter", 12),
                      fg_color="#EF4444", hover_color="#DC2626",
                      height=36, corner_radius=10, width=150,
                      command=lambda: self.app.show_screen("login")).pack(side="left", padx=5)

    # עושה תיבת סטטיסטיקה אחת
    def make_stat(self, parent, label, value, color, col):
        box = ctk.CTkFrame(parent, fg_color="transparent")
        box.grid(row=0, column=col, padx=20)
        ctk.CTkLabel(box, text=value, font=("Inter", 20, "bold"),
                     text_color=color).pack()
        ctk.CTkLabel(box, text=label, font=("Inter", 10),
                     text_color="#6B7280").pack()

    # חסימה/שחרור ישירות מהטבלה
    def do_toggle(self, acc_number):
        success, msg = self.app.bank.toggle_account(acc_number)
        if not success:
            messagebox.showerror("Error", msg)
            return
        self.app.save()
        # רענון המסך
        self.app.show_screen("admin")

    # הצגת היסטוריה של חשבון ספציפי
    def show_account_history(self, acc_number):
        account = self.app.bank.get_account(acc_number)
        if account is None:
            messagebox.showerror("Error", "Account not found")
            return

        win = ctk.CTkToplevel(self.app.root)
        win.title("History - " + account.name)
        win.geometry("450x400")
        win.configure(fg_color="#0A0E27")
        win.grab_set()

        ctk.CTkLabel(win, text="History: " + account.name + " (#" + acc_number + ")",
                     font=("Inter", 14, "bold"), text_color="white").pack(pady=(15, 8))

        history = account.history
        if len(history) == 0:
            ctk.CTkLabel(win, text="No transactions",
                         font=("Inter", 12), text_color="#6B7280").pack(pady=30)
            return

        scroll = ctk.CTkScrollableFrame(win, fg_color="#111827", corner_radius=10, height=280)
        scroll.pack(padx=15, pady=5, fill="both", expand=True)

        for record in reversed(history):
            rec_type = record["type"]
            if "deposit" in rec_type or "transfer_in" in rec_type:
                color = "#10B981"
                sign = "+"
            elif "withdraw" in rec_type or "transfer_out" in rec_type:
                color = "#EF4444"
                sign = "-"
            else:
                color = "#9CA3AF"
                sign = ""

            row = ctk.CTkFrame(scroll, fg_color="#0A0E27", corner_radius=4)
            row.pack(fill="x", pady=1)

            ctk.CTkLabel(row, text=record["date"], font=("Inter", 9),
                         text_color="#6B7280", width=110).pack(side="left", padx=4)

            type_text = rec_type
            if "target" in record:
                type_text = type_text + " #" + str(record["target"])
            ctk.CTkLabel(row, text=type_text, font=("Inter", 9),
                         text_color="#9CA3AF", width=100).pack(side="left", padx=4)

            ctk.CTkLabel(row, text=sign + str(record["amount"]),
                         font=("Inter", 9, "bold"),
                         text_color=color, width=70).pack(side="left", padx=4)

            ctk.CTkLabel(row, text="₪" + str(record["balance_after"]),
                         font=("Inter", 9),
                         text_color="#6B7280", width=70).pack(side="left", padx=4)

    # יצירת חשבון חדש
    def show_create(self):
        win = ctk.CTkToplevel(self.app.root)
        win.title("Create Account")
        win.geometry("350x380")
        win.configure(fg_color="#0A0E27")
        win.grab_set()

        ctk.CTkLabel(win, text="Create New Account",
                     font=("Inter", 16, "bold"), text_color="white").pack(pady=(20, 12))

        ctk.CTkLabel(win, text="Name", font=("Inter", 11),
                     text_color="#9CA3AF").pack(pady=(0, 2))
        name_entry = ctk.CTkEntry(win, font=("Inter", 13), fg_color="#1F2937",
                                  border_color="#374151", text_color="white",
                                  height=38, corner_radius=10, justify="center")
        name_entry.pack(padx=40, fill="x")

        ctk.CTkLabel(win, text="PIN (4 digits)", font=("Inter", 11),
                     text_color="#9CA3AF").pack(pady=(10, 2))
        pin_entry = ctk.CTkEntry(win, font=("Inter", 13), show="*", fg_color="#1F2937",
                                 border_color="#374151", text_color="white",
                                 height=38, corner_radius=10, justify="center")
        pin_entry.pack(padx=40, fill="x")

        ctk.CTkLabel(win, text="Initial Balance", font=("Inter", 11),
                     text_color="#9CA3AF").pack(pady=(10, 2))
        bal_entry = ctk.CTkEntry(win, font=("Inter", 13), fg_color="#1F2937",
                                 border_color="#374151", text_color="white",
                                 height=38, corner_radius=10, justify="center")
        bal_entry.pack(padx=40, fill="x")

        def do_create():
            name = name_entry.get()
            pin = pin_entry.get()
            bal = bal_entry.get()

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
            messagebox.showinfo("Success", "Account created!\nNumber: " + new_num)
            win.destroy()
            # רענון הפאנל
            self.app.show_screen("admin")

        ctk.CTkButton(win, text="Create Account", font=("Inter", 13, "bold"),
                      fg_color="#3B82F6", hover_color="#2563EB",
                      height=40, corner_radius=10,
                      command=do_create).pack(padx=40, pady=(16, 0), fill="x")
