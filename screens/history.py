import customtkinter as ctk
from tkinter import messagebox

# מסך היסטוריית עסקאות
class HistoryScreen(ctk.CTkFrame):
    def __init__(self, root, app):
        super().__init__(root, fg_color="#0A0E27", corner_radius=0)
        self.app = app
        self.account = app.current_account

        ctk.CTkLabel(self, text="Transaction History", font=("Inter", 20, "bold"),
                     text_color="white").pack(pady=(20, 4))

        ctk.CTkLabel(self, text="Account: " + self.account.account_number + " | " + self.account.name,
                     font=("Inter", 11), text_color="#6B7280").pack(pady=(0, 10))

        history = self.account.history

        if len(history) == 0:
            ctk.CTkLabel(self, text="No transactions yet",
                         font=("Inter", 13), text_color="#6B7280").pack(pady=40)
        else:
            # frame עם scroll
            scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#111827",
                                                   corner_radius=10, height=350)
            scroll_frame.pack(padx=20, pady=5, fill="both", expand=True)

            # כותרות
            header = ctk.CTkFrame(scroll_frame, fg_color="#1F2937", corner_radius=6)
            header.pack(fill="x", pady=(0, 4))
            ctk.CTkLabel(header, text="Date", font=("Inter", 10, "bold"),
                         text_color="#9CA3AF", width=120).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Type", font=("Inter", 10, "bold"),
                         text_color="#9CA3AF", width=90).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Amount", font=("Inter", 10, "bold"),
                         text_color="#9CA3AF", width=80).pack(side="left", padx=5)
            ctk.CTkLabel(header, text="Balance", font=("Inter", 10, "bold"),
                         text_color="#9CA3AF", width=80).pack(side="left", padx=5)

            # שורות - מהאחרונה לראשונה
            for record in reversed(history):
                # צבע לפי סוג עסקה
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

                row = ctk.CTkFrame(scroll_frame, fg_color="#0A0E27", corner_radius=4, height=30)
                row.pack(fill="x", pady=1)

                ctk.CTkLabel(row, text=record["date"], font=("Inter", 10),
                             text_color="#9CA3AF", width=120).pack(side="left", padx=5)

                # סוג + חשבון יעד אם יש
                type_text = rec_type
                if "target" in record:
                    type_text = type_text + " #" + str(record["target"])
                ctk.CTkLabel(row, text=type_text, font=("Inter", 10),
                             text_color="#D1D5DB", width=90).pack(side="left", padx=5)

                ctk.CTkLabel(row, text=sign + str(record["amount"]),
                             font=("Inter", 10, "bold"),
                             text_color=color, width=80).pack(side="left", padx=5)

                ctk.CTkLabel(row, text="₪" + str(record["balance_after"]),
                             font=("Inter", 10),
                             text_color="#6B7280", width=80).pack(side="left", padx=5)

        # כפתור חזרה
        ctk.CTkButton(self, text="Back", font=("Inter", 12),
                      fg_color="#374151", hover_color="#4B5563",
                      height=36, corner_radius=10,
                      command=lambda: self.app.show_screen("user_menu")).pack(pady=(10, 15))
