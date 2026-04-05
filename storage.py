import json
import os

DATA_FILE = "data.json"


def _init_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)


def load_json():
    _init_file()
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def write_json(updated_user):
    data = load_json()

    for i, user in enumerate(data):
        if user["id"] == updated_user["id"]:
            data[i] = updated_user
            break
    else:
        data.append(updated_user)

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
