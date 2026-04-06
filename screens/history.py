import tkinter as tk
from styles import COLORS, FONT_SUBTITLE, FONT_LABEL, FONT_TEXT

# מסך היסטוריית עסקאות
class HistoryScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg=COLORS["bg"])
        self.app = app
        self.account = app.current_account

        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Transaction History", font=FONT_SUBTITLE,
                 bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 5))

        tk.Frame(center, bg=COLORS["bg_light"], height=3, width=150).pack(pady=(0, 15))

        history = self.account.history

        if len(history) == 0:
            tk.Label(center, text="No transactions yet",
                     font=FONT_LABEL, bg=COLORS["bg"], fg=COLORS["text_light"]).pack(pady=20)
        else:
            # תיבת טקסט עם scrollbar
            frame = tk.Frame(center, bg=COLORS["bg"])
            frame.pack()

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side="right", fill="y")

            text_box = tk.Text(frame, font=FONT_TEXT, width=45, height=15,
                               bg=COLORS["bg_light"], fg=COLORS["white"],
                               relief="flat", yscrollcommand=scrollbar.set)
            text_box.pack()
            scrollbar.config(command=text_box.yview)

            # כותרת
            text_box.insert(tk.END, "  Date              | Type         | Amount\n")
            text_box.insert(tk.END, "  " + "-" * 44 + "\n")

            # עובר על כל עסקה מהאחרונה לראשונה
            for record in reversed(history):
                line = "  " + record["date"] + " | " + record["type"] + " | " + str(record["amount"])
                if "target" in record:
                    line = line + " (acc " + str(record["target"]) + ")"
                text_box.insert(tk.END, line + "\n")

            text_box.config(state="disabled")

        # חזרה
        tk.Button(center, text="Back", font=("Segoe UI", 11),
                  bg=COLORS["bg"], fg=COLORS["text_light"], relief="flat",
                  cursor="hand2", bd=0,
                  command=lambda: self.app.show_screen("user_menu")).pack(pady=(15, 0))
