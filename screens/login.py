import customtkinter as ctk
from tkinter import messagebox

# מסך כניסה - הראשון שרואים
class LoginScreen(ctk.CTkFrame):
    def __init__(self, root, app):
        super().__init__(root, fg_color="#0A0E27", corner_radius=0)
        self.app = app

        ctk.CTkLabel(self, text="ATM Machine", font=("Inter", 28, "bold"),
                     text_color="white").pack(pady=35)

        # כרטיס לבן שמחזיק את הטופס
        card = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        card.pack(padx=50, pady=10, fill="x")

        ctk.CTkLabel(card, text="Account Number", font=("Inter", 12),
                     text_color="#9CA3AF").pack(pady=(20, 4))
        self.acc_entry = ctk.CTkEntry(card, font=("Inter", 14),
                                      fg_color="#1F2937", border_color="#374151",
                                      text_color="white", height=40,
                                      corner_radius=10, justify="center")
        self.acc_entry.pack(padx=30, pady=(0, 12), fill="x")

        ctk.CTkLabel(card, text="PIN", font=("Inter", 12),
                     text_color="#9CA3AF").pack(pady=(0, 4))
        self.pin_entry = ctk.CTkEntry(card, font=("Inter", 14), show="*",
                                       fg_color="#1F2937", border_color="#374151",
                                       text_color="white", height=40,
                                       corner_radius=10, justify="center")
        self.pin_entry.pack(padx=30, pady=(0, 20), fill="x")

        ctk.CTkButton(self, text="Login", font=("Inter", 14, "bold"),
                      fg_color="#3B82F6", hover_color="#2563EB",
                      height=44, corner_radius=10,
                      command=self.handle_login).pack(padx=50, pady=8, fill="x")

        ctk.CTkButton(self, text="Admin Login", font=("Inter", 13),
                      fg_color="#EF4444", hover_color="#DC2626",
                      height=40, corner_radius=10,
                      command=self.handle_admin_login).pack(padx=50, pady=4, fill="x")

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

    # חלון קופץ לסיסמת מנהל
    def handle_admin_login(self):
        self.admin_win = ctk.CTkToplevel(self.app.root)
        self.admin_win.title("Admin Login")
        self.admin_win.geometry("320x220")
        self.admin_win.configure(fg_color="#0A0E27")
        self.admin_win.grab_set()

        ctk.CTkLabel(self.admin_win, text="Admin Password",
                     font=("Inter", 13), text_color="#9CA3AF").pack(pady=(20, 6))

        self.admin_pass_entry = ctk.CTkEntry(self.admin_win, font=("Inter", 14),
                                              show="*", fg_color="#111827",
                                              border_color="#374151",
                                              text_color="white", height=40,
                                              corner_radius=10, justify="center")
        self.admin_pass_entry.pack(padx=30, pady=(0, 16), fill="x")

        ctk.CTkButton(self.admin_win, text="Login", font=("Inter", 13),
                      fg_color="#EF4444", hover_color="#DC2626",
                      height=40, corner_radius=10,
                      command=self.check_admin_password).pack(padx=30, fill="x")

    def check_admin_password(self):
        password = self.admin_pass_entry.get()
        if password == self.app.bank.admin_password:
            self.admin_win.destroy()
            self.app.show_screen("admin")
        else:
            messagebox.showerror("Error", "Wrong admin password")