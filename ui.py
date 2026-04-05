import tkinter as tk
from tkinter import Listbox, Scrollbar, RIGHT, Y, BOTH, TOP, END
from models import Bank
from utils import now_str


BG = "#cfe3ff"
FG = "#003366"
BTN_BG = "#e6f0ff"
BTN_ACTIVE = "#d0e4ff"
TITLE_FONT = ("Arial", 18, "bold")
TEXT_FONT = ("Arial", 12)
BTN_FONT = ("Arial", 12, "bold")


def make_button(parent, text, cmd, width=25, bg=BTN_BG, fg=FG):
    return tk.Button(
        parent,
        text=text,
        command=cmd,
        width=width,
        bg=bg,
        fg=fg,
        activebackground=BTN_ACTIVE,
        font=BTN_FONT,
    )


def login_screen(root):
    bank = Bank()

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Welcome to Python ATM =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(frame, text="Enter ID", fg=FG, bg=BG, font=TEXT_FONT).pack(pady=8)
    id_entry = tk.Entry(
        frame,
        bg="#ffffff",
        fg="#000000",
        highlightbackground=FG,
        highlightcolor="#0066cc",
        highlightthickness=2,
    )
    id_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(
        frame, text="Enter password", fg=FG, bg=BG, font=TEXT_FONT
    ).pack(pady=8)
    pas_entry = tk.Entry(
        frame,
        bg="#ffffff",
        fg="#000000",
        highlightbackground=FG,
        highlightcolor="#0066cc",
        highlightthickness=2,
        show="*",
    )
    pas_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def do_login():
        user = bank.login(id_entry.get(), pas_entry.get())
        pas_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)

        if not user:
            status.config(text="Account not found")
            return

        if user.status == "disable":
            status.config(text="Account blocked!")
            return

        frame.pack_forget()
        user_menu(root, user)

    submit = make_button(frame, "Login", do_login, bg="#99c2ff")
    submit.pack(pady=20, ipady=5)

    root._bank = bank  


def user_menu(root, user):
    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text=f"Hello {user.name}",
        fg=FG,
        bg=BG,
        font=("Arial", 16, "bold"),
    ).pack(pady=15)

    if user.admin == "true":
        tk.Label(
            frame,
            text="You are admin",
            fg="#004c99",
            bg=BG,
            font=("Arial", 13, "bold"),
        ).pack(pady=10)

        make_button(
            frame,
            "Create account",
            lambda: create_account_screen(root, frame),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Disable account",
            lambda: disable_account_screen(root, frame),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Enable account",
            lambda: enable_account_screen(root, frame),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Account list",
            lambda: accounts_list_screen(root, frame),
        ).pack(pady=8, ipady=5)
    else:
        make_button(
            frame,
            "Balance",
            lambda: balance_screen(root, frame, user),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Withdraw Money",
            lambda: withdraw_screen(root, frame, user),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Deposit Money",
            lambda: deposit_screen(root, frame, user),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Bank Transfer",
            lambda: transfer_screen(root, frame, user),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "Change Password",
            lambda: change_password_screen(root, frame, user),
        ).pack(pady=8, ipady=5)
        make_button(
            frame,
            "History",
            lambda: history_screen(root, frame, user),
        ).pack(pady=8, ipady=5)

    make_button(
        frame,
        "Logout",
        lambda: logout_to_login(root, frame),
        bg="#f2d07a",
        fg="#660000",
    ).pack(pady=8, ipady=5)


def logout_to_login(root, frame):
    frame.destroy()
    login_screen(root)




def create_account_screen(root, prev):
    prev.pack_forget()
    bank = root._bank

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Create New Account =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(frame, text="Enter ID", fg=FG, bg=BG, font=TEXT_FONT).pack(pady=8)
    id_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    id_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(frame, text="Enter name", fg=FG, bg=BG, font=TEXT_FONT).pack(
        pady=8
    )
    name_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    name_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(frame, text="Is admin? y/n", fg=FG, bg=BG, font=TEXT_FONT).pack(
        pady=8
    )
    admin_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    admin_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    pin_label = tk.Label(frame, text="", fg="#006600", bg=BG, font=TEXT_FONT)
    pin_label.pack(pady=10)

    def submit():
        pin_label.config(text="")
        id_val = id_entry.get().strip()
        name_val = name_entry.get().strip()
        admin_val = admin_entry.get().strip().lower()

        if len(id_val) < 6:
            status.config(text="ID must contain at least 6 characters")
            return
        if len(name_val) < 4:
            status.config(text="Name must contain at least 4 characters")
            return
        if admin_val not in ("y", "n"):
            status.config(text="You must enter y/n")
            return

        is_admin = admin_val == "y"
        acc, pas = bank.create_account(id_val, name_val, is_admin)
        if not acc:
            status.config(text="Account with this ID already exists")
            return

        status.config(text="Account created successfully!")
        pin_label.config(text=f"User password: {pas}")

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu(root, frame),
    ).pack(pady=8, ipady=5)


def disable_account_screen(root, prev):
    prev.pack_forget()
    bank = root._bank

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Disable account =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(frame, text="Enter name", fg=FG, bg=BG, font=TEXT_FONT).pack(
        pady=8
    )
    name_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    name_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(frame, text="Enter ID", fg=FG, bg=BG, font=TEXT_FONT).pack(pady=8)
    id_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    id_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def submit():
        ok, msg = bank.disable_account(id_entry.get(), name_entry.get())
        status.config(text=msg)

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu(root, frame),
    ).pack(pady=8, ipady=5)


def enable_account_screen(root, prev):
    prev.pack_forget()
    bank = root._bank

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Enable account =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(frame, text="Enter name", fg=FG, bg=BG, font=TEXT_FONT).pack(
        pady=8
    )
    name_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    name_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(frame, text="Enter ID", fg=FG, bg=BG, font=TEXT_FONT).pack(pady=8)
    id_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    id_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def submit():
        ok, msg = bank.enable_account(id_entry.get(), name_entry.get())
        status.config(text=msg)

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu(root, frame),
    ).pack(pady=8, ipady=5)


def accounts_list_screen(root, prev):
    prev.pack_forget()
    bank = root._bank

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Account list =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    mylist = Listbox(
        frame,
        yscrollcommand=scrollbar.set,
        bg="#ffffff",
        fg=FG,
        font=TEXT_FONT,
    )

    num = 1
    for acc in bank.all_accounts():
        mylist.insert(
            END,
            f"{num}: Name={acc.name}, ID={acc.id}, Status={acc.status}, "
            f"Balance={acc.balance}, Admin={acc.admin}",
        )
        num += 1

    mylist.pack(side=TOP, fill=BOTH, expand=True)
    scrollbar.config(command=mylist.yview)

    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu(root, frame),
    ).pack(pady=8, ipady=5)


def back_to_user_menu(root, frame):
    frame.destroy()
    
    login_screen(root)


def balance_screen(root, prev, user):
    prev.pack_forget()
    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Balance =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(
        frame,
        text=f"{user.balance}",
        fg=FG,
        bg=BG,
        font=("Arial", 16, "bold"),
    ).pack(pady=10)

    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu_after_user(root, frame, user),
    ).pack(pady=8, ipady=5)


def back_to_user_menu_after_user(root, frame, user):
    frame.destroy()
    user_menu(root, user)


def deposit_screen(root, prev, user):
    prev.pack_forget()
    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Deposit =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(
        frame,
        text="Please type the amount you would like to deposit",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)

    amount_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    amount_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def submit():
        try:
            amount = float(amount_entry.get())
        except ValueError:
            status.config(text="Enter only numbers please")
            return
        if amount <= 0:
            status.config(text="Amount must be positive")
            return
        user.deposit(amount)
        amount_entry.delete(0, tk.END)
        status.config(text="Operation success!")

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu_after_user(root, frame, user),
    ).pack(pady=8, ipady=5)


def withdraw_screen(root, prev, user):
    prev.pack_forget()
    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Withdraw =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(
        frame,
        text="Please type the amount you would like to withdraw",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)

    amount_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    amount_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def submit():
        try:
            amount = float(amount_entry.get())
        except ValueError:
            status.config(text="Enter only numbers please")
            return
        if amount <= 0:
            status.config(text="Amount must be positive")
            return
        if not user.withdraw(amount):
            status.config(text="You don't have enough money")
            return
        amount_entry.delete(0, tk.END)
        status.config(text="Operation success!")

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu_after_user(root, frame, user),
    ).pack(pady=8, ipady=5)


def transfer_screen(root, prev, user):
    prev.pack_forget()
    bank = root._bank

    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Account transfer =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(
        frame,
        text="Please type the amount you would like to transfer",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)

    amount_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    amount_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(
        frame,
        text="Enter target account ID",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)

    id_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    id_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def submit():
        try:
            amount = float(amount_entry.get())
        except ValueError:
            status.config(text="Enter only numbers please")
            return
        if amount <= 0:
            status.config(text="Amount must be positive")
            return
        if id_entry.get() == user.id:
            status.config(text="Cannot transfer to yourself")
            return

        target = bank.find_by_id(id_entry.get())
        if not target:
            status.config(text="Target account not found")
            return

        if not user.transfer_to(target, amount):
            status.config(text="You don't have enough money")
            return

        amount_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)
        status.config(text="Operation success!")

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu_after_user(root, frame, user),
    ).pack(pady=8, ipady=5)


def change_password_screen(root, prev, user):
    prev.pack_forget()
    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= Change password =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    tk.Label(
        frame,
        text="Enter old password",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)
    old_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    old_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(
        frame,
        text="Enter new password",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)
    new_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    new_entry.pack(pady=5, ipadx=12, ipady=4)

    tk.Label(
        frame,
        text="Confirm new password",
        fg=FG,
        bg=BG,
        font=TEXT_FONT,
    ).pack(pady=8)
    confirm_entry = tk.Entry(frame, bg="#ffffff", fg="#000000")
    confirm_entry.pack(pady=5, ipadx=12, ipady=4)

    status = tk.Label(frame, text="", fg="#cc0000", bg=BG, font=TEXT_FONT)
    status.pack(pady=10)

    def submit():
        old = old_entry.get()
        new = new_entry.get()
        confirm = confirm_entry.get()

        if new != confirm:
            status.config(text="Passwords don't match")
            return
        if len(new) < 8:
            status.config(text="Password must contain at least 8 characters")
            return
        if not user.change_password(old, new):
            status.config(text="Old password incorrect")
            return

        old_entry.delete(0, tk.END)
        new_entry.delete(0, tk.END)
        confirm_entry.delete(0, tk.END)
        status.config(text="Operation success!")

    make_button(frame, "Submit", submit).pack(pady=20, ipady=5)
    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu_after_user(root, frame, user),
    ).pack(pady=8, ipady=5)


def history_screen(root, prev, user):
    prev.pack_forget()
    frame = tk.Frame(root, bg=BG)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="======= History =======",
        fg=FG,
        bg=BG,
        font=TITLE_FONT,
    ).pack(pady=20)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    mylist = Listbox(
        frame,
        yscrollcommand=scrollbar.set,
        bg="#ffffff",
        fg=FG,
        font=TEXT_FONT,
    )

    num = 1
    for line in user.history:
        mylist.insert(END, f"{num}: {line}")
        num += 1

    mylist.pack(side=TOP, fill=BOTH, expand=True)
    scrollbar.config(command=mylist.yview)

    make_button(
        frame,
        "Back",
        lambda: back_to_user_menu_after_user(root, frame, user),
    ).pack(pady=8, ipady=5)
