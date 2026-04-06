import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONT_SUBTITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON

# מסך שינוי PIN
class ChangePinScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg=COLORS["bg"])
        self.app = app

        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Change PIN", font=FONT_SUBTITLE,
                 bg=COLORS["bg"], fg=COLORS["white"]).pack(pady=(0, 5))

        tk.Frame(center, bg=COLORS["orange"], height=3, width=150).pack(pady=(0, 20))

        # PIN נוכחי
        tk.Label(center, text="Current PIN", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.old_pin = tk.Entry(center, font=FONT_ENTRY, justify="center", show="*",
                                bg=COLORS["bg_light"], fg=COLORS["white"],
                                insertbackground="white", relief="flat", width=22)
        self.old_pin.pack(pady=(3, 12), ipady=5)

        # PIN חדש
        tk.Label(center, text="New PIN", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.new_pin = tk.Entry(center, font=FONT_ENTRY, justify="center", show="*",
                                bg=COLORS["bg_light"], fg=COLORS["white"],
                                insertbackground="white", relief="flat", width=22)
        self.new_pin.pack(pady=(3, 12), ipady=5)

        # אימות
        tk.Label(center, text="Confirm New PIN", font=FONT_LABEL,
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack()
        self.confirm_pin = tk.Entry(center, font=FONT_ENTRY, justify="center", show="*",
                                    bg=COLORS["bg_light"], fg=COLORS["white"],
                                    insertbackground="white", relief="flat", width=22)
        self.confirm_pin.pack(pady=(3, 20), ipady=5)

        tk.Button(center, text="Change PIN", font=FONT_BUTTON,
                  bg=COLORS["orange"], fg=COLORS["white"], width=20,
                  relief="flat", cursor="hand2",
                  command=self.do_change).pack(ipady=4)

        tk.Button(center, text="Back", font=("Segoe UI", 11),
                  bg=COLORS["bg"], fg=COLORS["text_light"], relief="flat",
                  cursor="hand2", bd=0,
                  command=lambda: self.app.show_screen("user_menu")).pack(pady=(15, 0))

    def do_change(self):
        old = self.old_pin.get()
        new = self.new_pin.get()
        confirm = self.confirm_pin.get()

        if old == "" or new == "" or confirm == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        if new != confirm:
            messagebox.showerror("Error", "New PIN does not match")
            return

        success, msg = self.app.current_account.change_pin(old, new)
        if not success:
            messagebox.showerror("Error", msg)
            return

        self.app.save()
        messagebox.showinfo("Success", msg)
        self.app.show_screen("user_menu")
