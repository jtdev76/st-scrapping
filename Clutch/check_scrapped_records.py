import json

existing_records_file = open("scrapped_records.json", "r")

existing_records = json.loads(existing_records_file.read())

def check_records(name):
    if not existing_records.get(name):
        existing_records[name] = True
        return True
    else:
        return False

existing_records_write_file = open("scrapped_records.json", "w")
def save_records():
    existing_records_str = json.dumps(existing_records)
    existing_records_write_file.write(existing_records_str)