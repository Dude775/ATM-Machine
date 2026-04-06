import customtkinter as ctk
from tkinter import messagebox

class WithdrawScreen(ctk.CTkFrame):
    def __init__(self, root, app):
        super().__init__(root, fg_color="#0A0E27", corner_radius=0)
        self.app = app

        ctk.CTkLabel(self, text="Withdraw", font=("Inter", 22, "bold"),
                     text_color="white").pack(pady=(35, 5))

        ctk.CTkLabel(self, text="Current balance: ₪" + str(self.app.current_account.balance),
                     font=("Inter", 13), text_color="#9CA3AF").pack(pady=(0, 15))

        card = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        card.pack(padx=50, pady=5, fill="x")

        ctk.CTkLabel(card, text="Amount to withdraw",
                     font=("Inter", 12), text_color="#9CA3AF").pack(pady=(18, 4))

        self.amount_entry = ctk.CTkEntry(card, font=("Inter", 16),
                                          fg_color="#1F2937", border_color="#374151",
                                          text_color="white", height=44,
                                          corner_radius=10, justify="center",
                                          placeholder_text="0")
        self.amount_entry.pack(padx=25, pady=(0, 18), fill="x")

        ctk.CTkButton(self, text="Withdraw", font=("Inter", 14, "bold"),
                      fg_color="#3B82F6", hover_color="#2563EB",
                      height=44, corner_radius=10,
                      command=self.handle_withdraw).pack(padx=50, pady=(10, 5), fill="x")

        ctk.CTkButton(self, text="Back", font=("Inter", 12),
                      fg_color="#374151", hover_color="#4B5563",
                      height=38, corner_radius=10,
                      command=lambda: self.app.show_screen("user_menu")).pack(padx=50, pady=4, fill="x")

    def handle_withdraw(self):
        amount_str = self.amount_entry.get()

        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0")
            return

        # בדיקת יתרה - אי אפשר למשוך יותר ממה שיש
        if amount > self.app.current_account.balance:
            messagebox.showerror("Error", "Not enough balance")
            return

        self.app.current_account.withdraw(amount)
        self.app.save()
        messagebox.showinfo("Success", "Withdrew ₪" + str(amount))
        self.app.show_screen("user_menu")