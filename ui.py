from storage import save_data
import tkinter as tk
from tkinter import *
from tkinter import messagebox


class ATMApp:
    def __init__(self, root, bank):
        self.root = root
        self.bank = bank
        self.current_account = None
        self.logi = None
        self.upage = None
        self.identry = None
        self.pasentry = None
        self.status = None
        self._build_login()

    def _build_login(self):
        self.logi = tk.Frame(self.root, bg="#cfe3ff")
        self.logi.pack(fill="both", expand=True)
        label = tk.Label(self.logi, text="======= ATM =======", fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold"))
        label.pack(pady=20)
        id = tk.Label(self.logi, text="Enter id", fg="#003366", bg="#cfe3ff", font=("Arial", 12))
        id.pack(pady=8)
        self.identry = tk.Entry(self.logi, bg="#ffffff", fg="#000000", highlightbackground="#003366", highlightcolor="#0066cc", highlightthickness=2)
        self.identry.pack(pady=5, ipadx=12, ipady=4)
        pas = tk.Label(self.logi, text="Enter password", fg="#003366", bg="#cfe3ff", font=("Arial", 12))
        pas.pack(pady=8)
        self.pasentry = tk.Entry(self.logi, show="*", bg="#ffffff", fg="#000000", highlightbackground="#003366", highlightcolor="#0066cc", highlightthickness=2)
        self.pasentry.pack(pady=5, ipadx=12, ipady=4)
        submit = tk.Button(self.logi, text="login", width=25, bg="#99c2ff", fg="#003366", activebackground="#80b5ff", font=("Arial", 12, "bold"), command=lambda: self._log())
        submit.pack(pady=20, ipady=5)
        self.status = tk.Label(self.logi, text=f"", fg="#cc0000", bg="#cfe3ff", font=("Arial", 12))
        self.status.pack(pady=10)

    def _log(self):
        id_val = self.identry.get()
        paswo = self.pasentry.get()
        self.pasentry.delete(0, tk.END)
        self.identry.delete(0, tk.END)

        account = self.bank.login_user(id_val, paswo)

        if account is None:
            self._err()
            return

        save_data(self.bank)

        if account.status == "disable" or account.failed_attempts >= 3:
            self._ban()
            return
        if account.pin != paswo:
            self._attemp(account)
            return

        self.current_account = account
        self._show_user_page()

    def _ban(self):
        self.status.config(text=f"account blocked!", fg="#cc0000")

    def _attemp(self, account):
        self.status.config(text=f"wrong password!\n{3 - account.failed_attempts} more attempt", fg="#cc0000")

    def _err(self):
        self.status.config(text=f"account don't found", fg="#cc0000")

    def _logut(self):
        self.upage.destroy()
        self.logi.pack(fill="both", expand=True)
        self.status.config(text=f"")

    def _show_user_page(self):
        self.logi.pack_forget()
        self.upage = tk.Frame(self.root, bg="#cfe3ff")
        self.upage.pack(fill="both", expand=True)

        name = tk.Label(self.upage, text=f"hellow {self.current_account.name}", fg="#003366", bg="#cfe3ff", font=("Arial", 16, "bold"))
        name.pack(pady=15)

        if self.current_account.admin == "true":

            admin = tk.Label(self.upage, text=f"you are admin", fg="#004c99", bg="#cfe3ff", font=("Arial", 13, "bold"))
            admin.pack(pady=10)

            btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366", "activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}

            badd = tk.Button(self.upage, text="Create account", command=lambda: AdminPanel(self.root, self.upage, self.bank).baseui("create"), **btn_style)
            bdisable = tk.Button(self.upage, text="Disable account", command=lambda: AdminPanel(self.root, self.upage, self.bank).baseui("disable"), **btn_style)
            benable = tk.Button(self.upage, text="Enbale account", command=lambda: AdminPanel(self.root, self.upage, self.bank).baseui("enable"), **btn_style)
            baccounts = tk.Button(self.upage, text="Account list", command=lambda: AdminPanel(self.root, self.upage, self.bank).baseui("seeall"), **btn_style)
            blogout = tk.Button(self.upage, text="Logout", command=self._logut, bg="#f2d07a", fg="#660000", activebackground="#ff9090", font=("Arial", 12, "bold"), width=25)

            badd.pack(pady=8, ipady=5)
            bdisable.pack(pady=8, ipady=5)
            benable.pack(pady=8, ipady=5)
            baccounts.pack(pady=8, ipady=5)
            blogout.pack(pady=8, ipady=5)

        else:

            btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366", "activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}

            bbalance = tk.Button(self.upage, text="Balance", command=lambda: UserPanel(self.current_account, self.root, self.upage, self.bank).baseui("balance"), **btn_style)
            bwithdraw = tk.Button(self.upage, text="Withdraw Money", command=lambda: UserPanel(self.current_account, self.root, self.upage, self.bank).baseui("withdraw"), **btn_style)
            bdeposite = tk.Button(self.upage, text="Deposite Money", command=lambda: UserPanel(self.current_account, self.root, self.upage, self.bank).baseui("deposite"), **btn_style)
            bmove = tk.Button(self.upage, text="Bank Transfer", command=lambda: UserPanel(self.current_account, self.root, self.upage, self.bank).baseui("move"), **btn_style)
            bchange = tk.Button(self.upage, text="Change Password ", command=lambda: UserPanel(self.current_account, self.root, self.upage, self.bank).baseui("changepas"), **btn_style)
            bhistory = tk.Button(self.upage, text="History", command=lambda: UserPanel(self.current_account, self.root, self.upage, self.bank).baseui("history"), **btn_style)
            blogout = tk.Button(self.upage, text="Logout", command=self._logut, bg="#f2d07a", fg="#660000", activebackground="#ff9090", font=("Arial", 12, "bold"), width=25)

            bbalance.pack(pady=8, ipady=5)
            bwithdraw.pack(pady=8, ipady=5)
            bdeposite.pack(pady=8, ipady=5)
            bmove.pack(pady=8, ipady=5)
            bchange.pack(pady=8, ipady=5)
            bhistory.pack(pady=8, ipady=5)
            blogout.pack(pady=8, ipady=5)


class AdminPanel:
    def __init__(self, root, upage, bank):
        self.root = root
        self.upage = upage
        self.bank = bank

    def baseui(self, choose):

        self.upage.pack_forget()
        self.root = tk.Frame(self.root, bg="#cfe3ff")
        self.root.pack(fill="both", expand=True)
        self.root.configure(bg="#cfe3ff")

        if choose == "create":
            AdminPanel.create(self)
        elif choose == "disable":
            AdminPanel.disable(self)
        elif choose == "enable":
            AdminPanel.enable(self)
        elif choose == "seeall":
            AdminPanel.seeall(self)

        btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366", "activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}
        blogout = tk.Button(self.root, text="Back", command=lambda: AdminPanel.exit(self), **btn_style)
        blogout.pack(pady=8, ipady=5)

    def exit(self):
        self.root.destroy()
        self.upage.pack(fill="both", expand=True)

    def create(self):

        tk.Label(self.root, text="======= Create New Account =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Enter id",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        id = tk.Entry(self.root,
                    bg="#ffffff", fg="#000000",
                    highlightbackground="#003366",
                    highlightcolor="#0066cc",
                    highlightthickness=2)
        id.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Enter name",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        name = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        name.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Is admin? y/n",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        admin = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        admin.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)


        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.bank.add_account(admin.get(), name.get(), id.get())
            save_data(self.bank)
            status.config(text=result)
            id.delete(0, tk.END)
            name.delete(0, tk.END)
            admin.delete(0, tk.END)


    def disable(self):

        tk.Label(self.root, text="======= Disable account=======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Enter name",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        name = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        name.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Enter ID",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        id = tk.Entry(self.root,
                    bg="#ffffff", fg="#000000",
                    highlightbackground="#003366",
                    highlightcolor="#0066cc",
                    highlightthickness=2)
        id.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)

        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.bank.toggle_account(name.get(), id.get(), "disable")
            save_data(self.bank)
            status.config(text=result)
            id.delete(0, tk.END)
            name.delete(0, tk.END)


    def enable(self):

        tk.Label(self.root, text="======= Enable account=======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Enter name",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        name = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        name.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Enter ID",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        id = tk.Entry(self.root,
                    bg="#ffffff", fg="#000000",
                    highlightbackground="#003366",
                    highlightcolor="#0066cc",
                    highlightthickness=2)
        id.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)

        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.bank.toggle_account(name.get(), id.get(), "enable")
            save_data(self.bank)
            status.config(text=result)
            id.delete(0, tk.END)
            name.delete(0, tk.END)


    def seeall(self):

        tk.Label(self.root, text="======= Account lists=======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill=Y)

        mylist = Listbox(self.root,
                        yscrollcommand=scrollbar.set,
                        bg="#ffffff", fg="#003366",
                        font=("Arial", 12))

        for info in self.bank.get_all_accounts_info():
            mylist.insert(END, info)

        mylist.pack(side=TOP, fill=BOTH, expand=True)
        scrollbar.config(command=mylist.yview)


class UserPanel:
    def __init__(self, account, root, upage, bank):
        self.current_account = account
        self.root = root
        self.upage = upage
        self.bank = bank

    def baseui(self, choose):

        self.upage.pack_forget()
        self.root = tk.Frame(self.root, bg="#cfe3ff")
        self.root.pack(fill="both", expand=True)
        self.root.configure(bg="#cfe3ff")

        if choose == "balance":
            UserPanel.Balance(self)
        elif choose == "withdraw":
            UserPanel.withdraw(self)
        elif choose == "deposite":
            UserPanel.deposite(self)
        elif choose == "move":
            UserPanel.move(self)
        elif choose == "changepas":
            UserPanel.changepas(self)
        elif choose == "history":
            UserPanel.history(self)

        btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366", "activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}
        blogout = tk.Button(self.root, text="Back", command=lambda: UserPanel.exit(self), **btn_style)
        blogout.pack(pady=8, ipady=5)

    def exit(self):
        self.root.destroy()
        self.upage.pack(fill="both", expand=True)


    def Balance(self):

        tk.Label(self.root, text="======= Balance =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text=f"{self.current_account.balance}",
                fg="#003366", bg="#cfe3ff", font=("Arial", 16, "bold")
        ).pack(pady=10)



    def deposite(self):

        tk.Label(self.root, text="======= Deposite=======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Please type the amount you would like to deposite",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        amount = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        amount.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)

        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.current_account.deposit(amount.get())
            save_data(self.bank)
            status.config(text=result)
            amount.delete(0, tk.END)


    def withdraw(self):

        tk.Label(self.root, text="======= Withdraw =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Please type the amount you would like to withdraw",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        amount = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        amount.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)


        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.current_account.withdraw(amount.get())
            save_data(self.bank)
            status.config(text=result)
            amount.delete(0, tk.END)


    def move(self):

        tk.Label(self.root, text="======= Account transfer =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="Please type the amount you would like to  transfer",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        amount = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        amount.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Enter account id",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        id = tk.Entry(self.root,
                    bg="#ffffff", fg="#000000",
                    highlightbackground="#003366",
                    highlightcolor="#0066cc",
                    highlightthickness=2)
        id.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)

        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.bank.transfer(self.current_account, amount.get(), id.get())
            save_data(self.bank)
            status.config(text=result)
            amount.delete(0, tk.END)
            id.delete(0, tk.END)


    def changepas(self):

        tk.Label(self.root, text="======= Change password =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text="enter old password",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        old = tk.Entry(self.root,
                    bg="#ffffff", fg="#000000",
                    highlightbackground="#003366",
                    highlightcolor="#0066cc",
                    highlightthickness=2)
        old.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Enter password",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        pas = tk.Entry(self.root,
                    bg="#ffffff", fg="#000000",
                    highlightbackground="#003366",
                    highlightcolor="#0066cc",
                    highlightthickness=2)
        pas.pack(pady=5, ipadx=12, ipady=4)

        tk.Label(self.root, text="Enter password agin",
                fg="#003366", bg="#cfe3ff", font=("Arial", 12)
        ).pack(pady=8)

        pasv = tk.Entry(self.root,
                        bg="#ffffff", fg="#000000",
                        highlightbackground="#003366",
                        highlightcolor="#0066cc",
                        highlightthickness=2)
        pasv.pack(pady=5, ipadx=12, ipady=4)

        tk.Button(self.root, text="submit", width=25,
                bg="#e6f0ff", fg="#003366",
                activebackground="#d0e4ff",
                font=("Arial", 12, "bold"),
                command=lambda: submit()
        ).pack(pady=20, ipady=5)

        status = tk.Label(self.root, text=f"",
                        fg="#cc0000", bg="#cfe3ff",
                        font=("Arial", 12))
        status.pack(pady=10)

        def submit():
            messagebox.askquestion("validation","Are you sure?")
            result = self.current_account.change_pin(old.get(), pas.get(), pasv.get())
            save_data(self.bank)
            status.config(text=result)
            old.delete(0, tk.END)
            pas.delete(0, tk.END)
            pasv.delete(0, tk.END)


    def history(self):

        tk.Label(self.root, text="======= History =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill=Y)

        mylist = Listbox(self.root,
                        yscrollcommand=scrollbar.set,
                        bg="#ffffff", fg="#003366",
                        font=("Arial", 12))

        num = 0
        for sec in self.current_account.history:
            num += 1
            mylist.insert(END, f"{num}: {sec}")

        mylist.pack(side=TOP, fill=BOTH, expand=True)
        scrollbar.config(command=mylist.yview)
