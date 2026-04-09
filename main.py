import tkinter as tk
from models import Bank
from storage import load_data
from ui import ATMApp

bank = Bank()
load_data(bank)

root = tk.Tk()
root.geometry('800x600')
root.configure(bg="#152131")

ATMApp(root, bank)
root.mainloop()
