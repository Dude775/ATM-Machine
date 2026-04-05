import tkinter as tk
from ui import login_screen

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Python ATM")
    root.geometry("800x600")
    root.configure(bg="#cfe3ff")

    login_screen(root)

    root.mainloop()
