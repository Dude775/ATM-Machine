import customtkinter as ctk
from tkinter import messagebox

class ChangePinScreen(ctk.CTkFrame):
    def __init__(self, root, app):
        super().__init__(root, fg_color="#0A0E27", corner_radius=0)
        self.app = app

        ctk.CTkLabel(self, text="Change PIN", font=("Inter", 22, "bold"),
                     text_color="white").pack(pady=(35, 20))

        card = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        card.pack(padx=50, pady=5, fill="x")

        ctk.CTkLabel(card, text="Current PIN",
                     font=("Inter", 12), text_color="#9CA3AF").pack(pady=(18, 4))
        self.old_pin = ctk.CTkEntry(card, font=("Inter", 14), show="*",
                                     fg_color="#1F2937", border_color="#374151",
                                     text_color="white", height=40,
                                     corner_radius=10, justify="center")
        self.old_pin.pack(padx=25, pady=(0, 10), fill="x")

        ctk.CTkLabel(card, text="New PIN",
                     font=("Inter", 12), text_color="#9CA3AF").pack(pady=(0, 4))
        self.new_pin = ctk.CTkEntry(card, font=("Inter", 14), show="*",
                                     fg_color="#1F2937", border_color="#374151",
                                     text_color="white", height=40,
                                     corner_radius=10, justify="center")
        self.new_pin.pack(padx=25, pady=(0, 10), fill="x")

        ctk.CTkLabel(card, text="Confirm new PIN",
                     font=("Inter", 12), text_color="#9CA3AF").pack(pady=(0, 4))
        self.confirm_pin = ctk.CTkEntry(card, font=("Inter", 14), show="*",
                                         fg_color="#1F2937", border_color="#374151",
                                         text_color="white", height=40,
                                         corner_radius=10, justify="center")
        self.confirm_pin.pack(padx=25, pady=(0, 18), fill="x")

        ctk.CTkButton(self, text="Change PIN", font=("Inter", 14, "bold"),
                      fg_color="#3B82F6", hover_color="#2563EB",
                      height=44, corner_radius=10,
                      command=self.handle_change).pack(padx=50, pady=(10, 5), fill="x")

        ctk.CTkButton(self, text="Back", font=("Inter", 12),
                      fg_color="#374151", hover_color="#4B5563",
                      height=38, corner_radius=10,
                      command=lambda: self.app.show_screen("user_menu")).pack(padx=50, pady=4, fill="x")

    def handle_change(self):
        old = self.old_pin.get()
        new = self.new_pin.get()
        confirm = self.confirm_pin.get()

        if not old or not new or not confirm:
            messagebox.showerror("Error", "Please fill all fields")
            return

        # בדיקת ה-PIN הישן
        if not self.app.current_account.verify_pin(old):
            messagebox.showerror("Error", "Current PIN is wrong")
            return

        if new != confirm:
            messagebox.showerror("Error", "New PINs do not match")
            return

        # PIN צריך להיות לפחות 4 ספרות
        if len(new) < 4:
            messagebox.showerror("Error", "PIN must be at least 4 digits")
            return

        self.app.current_account.change_pin(new)
        self.app.save()
        messagebox.showinfo("Success", "PIN changed successfully")
        self.app.show_screen("user_menu")