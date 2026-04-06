import tkinter as tk
from tkinter import messagebox
from styles import COLORS, FONT_TITLE, FONT_LABEL, FONT_ENTRY, FONT_BUTTON, FONT_BUTTON_SM


class LoginScreen(tk.Frame):
    def __init__(self, root, app):
        tk.Frame.__init__(self, root, bg=COLORS["bg"])
        self.app = app
        self.adminwin = None

        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="ATM Machine",
            font=FONT_TITLE,
            bg=COLORS["bg"],
            fg=COLORS["white"]
        ).pack(pady=(0, 5))

        tk.Frame(
            center,
            bg=COLORS["green"],
            height=3,
            width=200
        ).pack(pady=(0, 25))

        tk.Label(
            center,
            text="Account Number",
            font=FONT_LABEL,
            bg=COLORS["bg"],
            fg=COLORS["text_light"]
        ).pack()

        self.accentry = tk.Entry(
            center,
            font=FONT_ENTRY,
            justify="center",
            bg=COLORS["bg_light"],
            fg=COLORS["white"],
            insertbackground="white",
            relief="flat",
            width=22
        )
        self.accentry.pack(pady=(3, 15), ipady=5)

        tk.Label(
            center,
            text="PIN",
            font=FONT_LABEL,
            bg=COLORS["bg"],
            fg=COLORS["text_light"]
        ).pack()

        self.pinentry = tk.Entry(
            center,
            font=FONT_ENTRY,
            justify="center",
            show="*",
            bg=COLORS["bg_light"],
            fg=COLORS["white"],
            insertbackground="white",
            relief="flat",
            width=22
        )
        self.pinentry.pack(pady=(3, 25), ipady=5)

        tk.Button(
            center,
            text="Login",
            font=FONT_BUTTON,
            bg=COLORS["green"],
            fg=COLORS["white"],
            width=20,
            relief="flat",
            cursor="hand2",
            activebackground=COLORS["green_dark"],
            activeforeground="white",
            command=self.handlelogin
        ).pack(pady=(0, 10), ipady=4)

        tk.Button(
            center,
            text="Admin Panel",
            font=FONT_BUTTON_SM,
            bg=COLORS["bg"],
            fg=COLORS["red"],
            width=20,
            relief="flat",
            cursor="hand2",
            bd=0,
            activebackground=COLORS["bg"],
            activeforeground=COLORS["red_dark"],
            command=self.handleadminlogin
        ).pack(pady=(5, 0))

    def handlelogin(self):
        accnumber = self.accentry.get()
        pin = self.pinentry.get()

        account = self.app.bank.get_account(accnumber)

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

    def handleadminlogin(self):
        if self.adminwin is not None and self.adminwin.winfo_exists():
            self.adminwin.lift()
            self.adminwin.focus_force()
            return

        self.adminwin = tk.Toplevel(self.app.root)
        self.adminwin.title("Admin Login")
        self.adminwin.geometry("300x220")
        self.adminwin.configure(bg=COLORS["bg"])
        self.adminwin.resizable(False, False)
        self.adminwin.transient(self.app.root)
        self.adminwin.protocol("WM_DELETE_WINDOW", self.close_admin_window)

        center = tk.Frame(self.adminwin, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            center,
            text="Admin Login",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["bg"],
            fg=COLORS["white"]
        ).pack(pady=(0, 15))

        tk.Label(
            center,
            text="Password",
            font=FONT_LABEL,
            bg=COLORS["bg"],
            fg=COLORS["text_light"]
        ).pack()

        self.adminpassentry = tk.Entry(
            center,
            font=FONT_ENTRY,
            justify="center",
            show="*",
            bg=COLORS["bg_light"],
            fg=COLORS["white"],
            insertbackground="white",
            relief="flat",
            width=20
        )
        self.adminpassentry.pack(pady=(3, 20), ipady=5)
        self.adminpassentry.focus_set()

        tk.Button(
            center,
            text="Login",
            font=FONT_BUTTON,
            bg=COLORS["red"],
            fg=COLORS["white"],
            width=18,
            relief="flat",
            cursor="hand2",
            activebackground=COLORS["red_dark"],
            command=self.checkadminpassword
        ).pack(ipady=3)

    def checkadminpassword(self):
        password = self.adminpassentry.get()

        if password == self.app.bank.admin_password:
            self.close_admin_window()
            self.app.show_screen("admin")
        else:
            messagebox.showerror("Error", "Wrong admin password")

    def close_admin_window(self):
        if self.adminwin is not None and self.adminwin.winfo_exists():
            self.adminwin.destroy()
        self.adminwin = None