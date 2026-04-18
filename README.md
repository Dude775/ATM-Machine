# ATM Machine

A simple ATM banking simulator with a GUI, built as a pair project for the IITC DevOps Python course.

## What it does

The app simulates an ATM with two types of users:

**Regular user:**
- Check balance
- Deposit / withdraw money
- Transfer money to another account
- View transaction history
- Change password

**Admin:**
- Create new accounts (password is auto-generated)
- Enable / disable accounts
- View all accounts in the system

Login locks after 4 failed attempts. Data is saved to a local JSON file so everything persists between runs.

## How to run

```bash
git clone https://github.com/Dude775/ATM-Machine.git
cd ATM-Machine
python main.py
```

No pip install needed - only standard library (tkinter, json, secrets).

## Project structure

```
ATM-Machine/
├── main.py      # entry point, starts the app
├── models.py    # Bank and Account classes, OOP stuff
├── storage.py   # saves and loads data.json
├── ui.py        # all the GUI screens
└── login.py     # original login screen (mostly replaced by ui.py)
```

## Built with

- Python 3
- tkinter (GUI)
- json + secrets (standard library only)

## What we learned

This was our first real OOP project in Python. Getting the inheritance to work between `BankEntity`, `Account`, and `Bank` took some time to figure out. The GUI part with tkinter was also new - managing which frame is visible at any point was a bit tricky. File persistence with JSON ended up being simpler than expected.

Overall a good project to understand how a real app is structured with separate files for models, storage, and UI.

---

*Pair project - David Rubin + partner | IITC DevOps course*
