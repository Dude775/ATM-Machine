import customtkinter as ctk
from app import ATMApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = ATMApp(root)
    root.mainloop()