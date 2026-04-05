import secrets
import string
import datetime


def secure_random_string(length=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def now_str():
    x = datetime.datetime.now()
    return x.strftime("%c")
