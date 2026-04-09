from storage import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox 
from models import *


class bank:
    def __init__(self,root,upage):
        self.root = root
        self.upage = upage

    def baseui(self,choose):
        
        self.upage.pack_forget()
        self.root = tk.Frame(self.root, bg="#cfe3ff")
        self.root.pack(fill="both", expand=True)
        self.root.configure(bg="#cfe3ff")

        if choose == "create":
            bank.create(self)
        elif choose == "disable":
            bank.disable(self)
        elif choose == "enable":
            bank.enable(self)
        elif choose == "seeall":
           bank.seeall(self)

        btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366","activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}
        blogout = tk.Button(self.root, text="Back", command=lambda: bank.exit(self),**btn_style)
        blogout.pack(pady=8, ipady=5)
        self.root.mainloop()   
    
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
            result = cre(admin.get(), name.get(), id.get())
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
            result = des(name.get(), id.get())
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
            result = enb(name.get(), id.get())
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
        
        num = 1
        with open('data.json', 'r+') as file:
            file_data = json.load(file)

        for account in file_data:
            mylist.insert(END,
                        f"{num}: Name = {account['name']}, ID = {account['id']}, Status = {account['status']}, Balance = {account['balance']:,}, Admin = {account['admin']}")
            num += 1

        mylist.pack(side=TOP, fill=BOTH, expand=True)
        scrollbar.config(command=mylist.yview)





class user:
    def __init__(self,account,root,upage):
        self.account = account
        self.root = root
        self.upage = upage

    def baseui(self,choose):
        
        self.upage.pack_forget()
        self.root = tk.Frame(self.root, bg="#cfe3ff")
        self.root.pack(fill="both", expand=True)
        self.root.configure(bg="#cfe3ff")

        if choose == "balance":
            user.Balance(self)
        elif choose == "withdraw":
            user.withdraw(self)
        elif choose == "deposite":
            user.deposite(self)
        elif choose == "move":
            user.move(self)
        elif choose == "changepas":
            user.changepas(self)
        elif choose == "history":
            user.history(self)

        btn_style = {"width": 25, "bg": "#e6f0ff", "fg": "#003366","activebackground": "#d0e4ff", "font": ("Arial", 12, "bold")}
        blogout = tk.Button(self.root, text="Back", command=lambda: user.exit(self),**btn_style)
        blogout.pack(pady=8, ipady=5)
        self.root.mainloop()   
    
    def exit(self):
        self.root.destroy()
        self.upage.pack(fill="both", expand=True)


    def Balance(self):

        tk.Label(self.root, text="======= Balance =======",
                fg="#003366", bg="#cfe3ff", font=("Arial", 18, "bold")
        ).pack(pady=20)

        tk.Label(self.root, text=f"{self.account['balance']}",
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
            result = dep(self, amount.get())
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
            result = wit(self, amount.get())
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
            result = mov(self, amount.get(), id.get())
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
            result = change(self, old.get(), pas.get(), pasv.get())
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

        with open('data.json', 'r+') as file:
            file_data = json.load(file)

        for account in file_data:
            if account["id"] == self.account["id"] and account["pas"] == self.account["pas"]:
                num = 0
                for sec in account["history"]:
                    num += 1
                    mylist.insert(END, f"{num}: {sec}")

        mylist.pack(side=TOP, fill=BOTH, expand=True)
        scrollbar.config(command=mylist.yview)

       
        
   
        



