import json


def write(key, value, add_or_write="write"):
    with open("db.json") as f:
        sl = json.load(f)
    with open("db.json", "w") as f:
        if add_or_write == "write":
            sl[key] = value
        if add_or_write == "add" and key in sl:
            sl[key] += value
        json.dump(sl, f)


def read(key):
    with open("db.json") as f:
        sl = json.load(f)
    return sl.get(key, None)
