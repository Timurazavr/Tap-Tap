import json


def read(key):
    with open("db.json") as f:
        sl = json.load(f)
    return sl.get(key, None)


def all_read():
    with open("db.json") as f:
        return json.load(f)


def all_write(sl):
    with open("db.json", "w") as f:
        json.dump(sl, f)
