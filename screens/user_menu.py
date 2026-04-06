import customtkinter as ctk

# תפריט ראשי - מציג יתרה וכפתורי פעולות
class UserMenuScreen(ctk.CTkFrame):
    def __init__(self, root, app):
        super().__init__(root, fg_color="#0A0E27", corner_radius=0)
        self.app = app

        name = self.app.current_account.name
        balance = self.app.current_account.balance

        ctk.CTkLabel(self, text="Welcome, " + name, font=("Inter", 20, "bold"),
                     text_color="white").pack(pady=(30, 4))

        # כרטיס יתרה
        balance_card = ctk.CTkFrame(self, fg_color="#111827", corner_radius=12)
        balance_card.pack(padx=50, pady=8, fill="x")

        ctk.CTkLabel(balance_card, text="Current Balance",
                     font=("Inter", 11), text_color="#6B7280").pack(pady=(14, 2))
        self.balance_label = ctk.CTkLabel(balance_card,
                     text="₪ " + str(balance),
                     font=("Inter", 26, "bold"), text_color="#3B82F6")
        self.balance_label.pack(pady=(0, 14))

        # כפתורי פעולות
        buttons = [
            ("Deposit",     "#3B82F6", "#2563EB", "deposit"),
            ("Withdraw",    "#3B82F6", "#2563EB", "withdraw"),
            ("Transfer",    "#3B82F6", "#2563EB", "transfer"),
            ("History",     "#374151", "#4B5563", "history"),
            ("Change PIN",  "#374151", "#4B5563", "change_pin"),
        ]

        for label, color, hover, screen in buttons:
            ctk.CTkButton(self, text=label, font=("Inter", 13),
                          fg_color=color, hover_color=hover,
                          height=40, corner_radius=10,
                          command=lambda s=screen: self.app.show_screen(s)
                          ).pack(padx=50, pady=4, fill="x")

        # TODO: logout בתחתית - נראה יותר טבעי
        ctk.CTkButton(self, text="Logout", font=("Inter", 12),
                      fg_color="#EF4444", hover_color="#DC2626",
                      height=38, corner_radius=10,
                      command=self.app.logout).pack(padx=50, pady=(8, 20), fill="x")