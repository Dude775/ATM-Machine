import tkinter as tk
from ui import *
from models import login

root = tk.Tk()
root.geometry('800x600')
root.configure(bg="#152131") 
logi = tk.Frame(root, bg="#cfe3ff")
logi.pack(fill="both", expand=True)
label = tk.Label(logi, text="======= ATM =======",fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold"))
label.pack(pady=20)
id = tk.Label(logi, text="Enter id", fg="#003366", bg="#cfe3ff", font=("Arial", 12))
id.pack(pady=8)
identry = tk.Entry(logi, bg="#ffffff", fg="#000000",highlightbackground="#003366", highlightcolor="#0066cc", highlightthickness=2)
identry.pack(pady=5, ipadx=12, ipady=4)
pas = tk.Label(logi, text="Enter password", fg="#003366", bg="#cfe3ff", font=("Arial", 12))
pas.pack(pady=8)
pasentry = tk.Entry(logi,show="*", bg="#ffffff", fg="#000000",highlightbackground="#003366", highlightcolor="#0066cc", highlightthickness=2)
pasentry.pack(pady=5, ipadx=12, ipady=4)


def log():
    global account
    account = login(identry.get(), pasentry.get())
    paswo = pasentry.get()
    pasentry.delete(0, tk.END)
    identry.delete(0, tk.END)
    if account:
        if account["status"] == "disable" or account["attempt"] > 4:
            ban()
        elif account["attempt"] <= 4 and account["pas"] != paswo:
            attemp()
       
        else:
            logi.pack_forget()
            global upage
            upage = tk.Frame(root, bg="#cfe3ff")
            upage.pack(fill="both", expand=True)

            name = tk.Label(upage, text=f"hellow {account['name']}",fg="#003366", bg="#cfe3ff", font=("Arial", 16, "bold"))
            name.pack(pady=15)

            if account["admin"] == "true":

                admin = tk.Label(upage, text=f"you are admin",fg="#004c99", bg="#cfe3ff", font=("Arial", 13, "bold"))
                admin.pack(pady=10)

                btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366","activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}
                
                badd = tk.Button(upage, text="Create account", command=lambda: bank(root,upage).baseui("create"), **btn_style)
                bdisable = tk.Button(upage, text="Disable account", command=lambda: bank(root,upage).baseui("disable"), **btn_style)
                benable = tk.Button(upage, text="Enbale account", command=lambda: bank(root,upage).baseui("enable"), **btn_style)
                baccounts = tk.Button(upage, text="Account list", command=lambda: bank(root,upage).baseui("seeall"), **btn_style)
                blogout = tk.Button(upage, text="Logout", command=logut,bg="#f2d07a", fg="#660000", activebackground="#ff9090",font=("Arial", 12, "bold"), width=25)

                badd.pack(pady=8, ipady=5)
                bdisable.pack(pady=8, ipady=5)
                benable.pack(pady=8, ipady=5)
                baccounts.pack(pady=8, ipady=5)
                blogout.pack(pady=8, ipady=5)

            else:

                btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366","activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}

                bbalance = tk.Button(upage, text="Balance", command=lambda: user(account,root,upage).baseui("balance"), **btn_style)
                bwithdraw = tk.Button(upage, text="Withdraw Money", command=lambda: user(account,root,upage).baseui("withdraw"), **btn_style)
                bdeposite = tk.Button(upage, text="Deposite Money", command=lambda: user(account,root,upage).baseui("deposite"), **btn_style)
                bmove = tk.Button(upage, text="Bank Transfer", command=lambda: user(account,root,upage).baseui("move"), **btn_style)
                bchange = tk.Button(upage, text="Change Password ", command=lambda: user(account,root,upage).baseui("changepas"), **btn_style)
                bhistory = tk.Button(upage, text="History", command=lambda: user(account,root,upage).baseui("history"), **btn_style)
                blogout = tk.Button(upage, text="Logout", command=logut,bg="#f2d07a", fg="#660000", activebackground="#ff9090",font=("Arial", 12, "bold"), width=25)

                bbalance.pack(pady=8, ipady=5)
                bwithdraw.pack(pady=8, ipady=5)
                bdeposite.pack(pady=8, ipady=5)
                bmove.pack(pady=8, ipady=5)
                bchange.pack(pady=8, ipady=5)
                bhistory.pack(pady=8, ipady=5)
                blogout.pack(pady=8, ipady=5)

    else:
        err()

def ban():
    status.config(text=f"account blocked!", fg="#cc0000")

def attemp():
    status.config(text=f"you have {4-account["attempt"]} more attempt", fg="#cc0000")

def err():
    status.config(text=f"account don't found", fg="#cc0000")

def logut():
    upage.destroy()
    logi.pack(fill="both", expand=True)
    status.config(text=f"")

submit = tk.Button(logi, text="login", width=25,bg="#99c2ff", fg="#003366", activebackground="#80b5ff",font=("Arial", 12, "bold"), command=lambda: log())
submit.pack(pady=20, ipady=5)
status = tk.Label(logi, text=f"", fg="#cc0000", bg="#cfe3ff", font=("Arial", 12))
status.pack(pady=10)

root.mainloop()