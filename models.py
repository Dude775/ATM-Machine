from storage import *
import tkinter as tk
from tkinter import *
import datetime
import secrets
import string
from tkinter import messagebox 
from models import *

def login(id,pas):
        with open('data.json', 'r+') as file:
            file_data = json.load(file)
        for account in file_data:
            if account["id"] == id and account["pas"] == pas:
                if account["attempt"] <= 4:
                    account["attempt"] = 0
                    write_json(account)
                    return account
                else: 
                    write_json(account)
                    return account
            elif account["id"] == id and account["pas"] != pas:
                account["attempt"] += 1
                write_json(account)
                return account
            
        else: return None
        


        

def cre(pin,admin,name,id):
            pin.config(text="")
            with open("data.json", 'r+') as file:
                file_data = json.load(file)
                for account in file_data:
                    if account["id"] == id.get():
                        return "already have accound with the same id"
                        
                if len(id.get()) < 6:
                    return "id must containe 6 characters"
                   
                                        
                if len(name.get()) < 4:
                    return "name must containe 4 characters"
                    
                        
                if admin.get() != "y" and admin.get() != "n":
                    return "you must enter y/n!"
                    

                if admin.get() == "y":
                    admin_value = "true"
                elif admin.get() == "n":
                    admin_value = "false"
            pas = secure_random_string()

            new_account = {
                "id": id.get(),
                "pas": pas,
                "name": name.get(),
                "balance": 0,
                "admin": admin_value,
                "status": "enable",
                "history": [],
                "attemp": 0
            }

            with open("data.json", 'r+') as file:
                file_data = json.load(file)
                write_json(new_account)
                return "success!\nuser password: " + pas
        


def secure_random_string(length=16):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))


def des(name, id):
            with open('data.json', 'r+') as file:
                file_data = json.load(file)
            for account in file_data:
                if account["id"] == id.get() and account["name"] == name.get() :
                    if account["admin"] == "false":
                        account["status"] = "disable"
                        write_json(account)
                        return "Account disable!"
                    else:
                        return "Admin can't disable itself!!"
                else:
                    return "account don't found!"



def enb(name, id):
            found = ""
            with open('data.json', 'r+') as file:
                file_data = json.load(file)
            for account in file_data:
                if account["id"] == id.get() and account["name"] == name.get():
                    account["status"] = "enable"
                    write_json(account)
                    found = "yes"
                    return "Account enable!"
            if found != "yes":
                return "account don't found!"






def dep(self, amount):
            messagebox.askquestion("validation","Are you sure?")
            try:
                float(amount.get())
            except ValueError:
                return "enter only numbers please"
            else:
                if float(amount.get()) < 0:
                    return "You cannot tpye negative numbers"
                else:
                    self.account["balance"] += float(amount.get())
                    x = datetime.datetime.now()
                    log = f"{x.strftime('%c')} you deposite {float(amount.get())}"
                    self.account["history"].append(log)
                    write_json(self.account)
                    amount.delete(0, tk.END)
                    return "operation success!"



def wit(self, amount):
            messagebox.askquestion("validation","Are you sure?")
            try:
                float(amount.get())
            except ValueError:
                return "enter only numbers please"
            else:
                if float(amount.get()) < 0:
                    return "You cannot tpye negative numbers"
                else:
                    with open("data.json", 'r+') as file:
                        file_data = json.load(file)
                        for account in file_data:
                            if account["id"] == self.account["id"] and account["pas"] == self.account["pas"]:
                                if account["balance"] - float(amount.get()) < 0:
                                    return "you dont have enough money"
                                else:
                                    self.account["balance"] -= float(amount.get())
                                    x = datetime.datetime.now()
                                    log = f"{x.strftime('%c')} you withdraw {float(amount.get())}"
                                    self.account["history"].append(log)
                                    write_json(self.account)
                                    amount.delete(0, tk.END)
                                    return "operation success!"


def mov(self, amount, id):
            messagebox.askquestion("validation","Are you sure?")
            try:
                float(amount.get())
            except ValueError:
                return "enter only numbers please"
            else:
                if float(amount.get()) < 0:
                    return "You cannot tpye negative numbers"
                else:
                    with open("data.json", 'r+') as file:
                        file_data = json.load(file)
                        for account in file_data:
                            if account["id"] == self.account["id"] and account["pas"] == self.account["pas"]:
                                if account["balance"] - float(amount.get()) < 0:
                                    return "you dont have enough money"
                                else:
                                    for account in file_data:
                                        if account["id"] == id.get() and id.get() != self.account["id"] :
                                            self.account["balance"] -= float(amount.get())
                                            x = datetime.datetime.now()
                                            log = f"{x.strftime('%c')} you send to account {id.get()} {float(amount.get())}"
                                            self.account["history"].append(log)
                                            write_json(self.account)

                                            account["balance"] += float(amount.get())
                                            log = f"{x.strftime('%c')} account {self.account['id']} send to you {float(amount.get())}"
                                            account["history"].append(log)
                                            write_json(account)

                                            amount.delete(0, tk.END)
                                            id.delete(0, tk.END)
                                            return "operation success!"
                                        else:
                                            if id.get() == self.account["id"]:
                                                return "you can't transfer to your account"
                                            else:
                                                return "account don't found!"


def change(self, old, pas, pasv):
            if old.get() != self.account["pas"]:
                return "old password incorrect"
            if pas.get() != pasv.get():
                return "password don't match"
            if len(pas.get()) < 8:
                return "password must containe 8 characters"

            self.account["pas"] = pas.get()
            write_json(self.account)

            old.delete(0, tk.END)
            pas.delete(0, tk.END)
            pasv.delete(0, tk.END)

            return "operation success!"
