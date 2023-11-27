# import json

# existing_records_file = open("scrapped_records.json", "w+")

# existing_records = json.loads(existing_records_file.read())

# def check_records(name):
#     if not existing_records.get(name):
#         existing_records[name] = True
#         return True
#     else:
#         return False

# def save_records():
#     existing_records_str = json.dumps(existing_records)
#     existing_records_file.write(existing_records_str)
import json

file_path = "scrapped_records.json"

try:
    with open(file_path, "r") as existing_records_file:
        existing_records = json.load(existing_records_file)
except (FileNotFoundError, json.JSONDecodeError):
    existing_records = {}

def check_records(name):
    if not existing_records.get(name):
        existing_records[name] = True
        return True
    else:
        return False

def save_records():
    with open(file_path, "w") as existing_records_file:
        json.dump(existing_records, existing_records_file)

# Example usage:
# if check_records("John"):
#     print("Record added for John.")
# else:
#     print("Record for John already exists.")
    
# Save the updated records back to the file
# save_records()
