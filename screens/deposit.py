import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONT_SUBTITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON

# מסך הפקדה
class DepositScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg=COLORS["bg"])
        self.app = app

        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Deposit", font=FONT_SUBTITLE,
                 bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 5))

        tk.Frame(center, bg=COLORS["green"], height=3, width=150).pack(pady=(0, 20))

        # יתרה נוכחית
        self.bal_label = tk.Label(center,
                 text="Current balance: $" + str(self.app.current_account.balance),
                 font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["green"])
        self.bal_label.pack(pady=(0, 15))

        tk.Label(center, text="Enter amount", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.amount_entry = tk.Entry(center, font=FONT_ENTRY, justify="center",
                                     bg=COLORS["bg_light"], fg=COLORS["white"],
                                     insertbackground="white", relief="flat", width=22)
        self.amount_entry.pack(pady=(3, 20), ipady=5)

        tk.Button(center, text="Deposit", font=FONT_BUTTON,
                  bg=COLORS["green"], fg=COLORS["white"], width=20,
                  relief="flat", cursor="hand2",
                  activebackground=COLORS["green_dark"],
                  command=self.do_deposit).pack(ipady=4)

        # חזרה
        tk.Button(center, text="Back", font=("Segoe UI", 11),
                  bg=COLORS["bg"], fg=COLORS["text_light"], relief="flat",
                  cursor="hand2", bd=0,
                  command=lambda: self.app.show_screen("user_menu")).pack(pady=(15, 0))

    def do_deposit(self):
        text = self.amount_entry.get()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount")
            return
        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        success, msg = self.app.current_account.deposit(amount)
        if not success:
            messagebox.showerror("Error", msg)
            return

        self.app.save()
        messagebox.showinfo("Success", msg)
        self.app.show_screen("user_menu")
