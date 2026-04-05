import tkinter as tk
from tkinter import messagebox

# מסך העברה בין חשבונות
class TransferScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg="#1a237e")
        self.app = app

        tk.Label(self, text="Transfer", font=("Segoe UI", 22, "bold"),
                 bg="#1a237e", fg="white").pack(pady=30)

        tk.Label(self, text="Target account number:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)

        self.target_entry = tk.Entry(self, font=("Segoe UI", 14), justify="center")
        self.target_entry.pack(pady=5)

        tk.Label(self, text="Amount:", font=("Segoe UI", 12),
                 bg="#1a237e", fg="white").pack(pady=5)

        self.amount_entry = tk.Entry(self, font=("Segoe UI", 14), justify="center")
        self.amount_entry.pack(pady=5)

        tk.Button(self, text="Transfer", font=("Segoe UI", 14),
                  bg="#ff9800", fg="white", width=15,
                  command=self.do_transfer).pack(pady=15)

        tk.Button(self, text="Back", font=("Segoe UI", 12),
                  bg="white", fg="#1a237e", width=15,
                  command=lambda: self.app.show_screen("user_menu")).pack(pady=5)

    def do_transfer(self):
        target = self.target_entry.get()
        text = self.amount_entry.get()

        if target == "" or text == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        # בדיקה שלא מעבירים לעצמך
        if target == self.app.current_account.account_number:
            messagebox.showerror("Error", "Cannot transfer to yourself")
            return
        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        # הלוגיקה של ההעברה נמצאת ב-Bank
        success, message = self.app.bank.transfer(self.app.current_account, target, amount)
        if not success:
            messagebox.showerror("Error", message)
            return

        self.app.save()
        messagebox.showinfo("Success", message)
        self.app.show_screen("user_menu")
