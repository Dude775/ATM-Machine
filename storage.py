import json

def write_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        for index, user in enumerate(file_data):
            if user["id"] == new_data["id"] and user["name"] == new_data["name"]:
                file_data[index] = new_data
                break
        else:file_data.append(new_data)
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)

