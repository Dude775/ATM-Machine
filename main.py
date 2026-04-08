import tkinter as tk
from models import Bank
from storage import load_data
from ui import ATMApp

# bank riyk — yitmaleh im yesh data.json
bank = Bank()
load_data(bank)

root = tk.Tk()
app = ATMApp(root, bank)
root.mainloop()
