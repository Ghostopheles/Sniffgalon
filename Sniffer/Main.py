import os
import csv
import operator

from datetime import datetime

from Dumper import get_dumpers

# dump raw response json
dump_raw = True

# dump csv with just id, name, and api url
dump_processed = True

all_dumpers = get_dumpers(dump_raw=dump_raw, dump_processed=dump_processed)

for dumper in all_dumpers:
    dumper.fetch_all()

timestamp = datetime.now().strftime("%Y-%m-%d")
dump_path = f"../Data/{timestamp}"


def get_key(row):
    id = row[0]
    if id != "id":
        return int(id)
    return 0


def handle_folder(folder_path: str):
    data_dir = os.path.join(folder_path, "Processed")
    if not os.path.exists(data_dir):
        return

    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        if file.endswith(".csv"):
            with open(file_path, "r", newline="") as f:
                reader = csv.reader(f, delimiter=",")
                sorted_csv_data = sorted(reader, key=get_key, reverse=False)

            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerows(sorted_csv_data)


for dir in os.listdir(dump_path):
    full_path = os.path.join(dump_path, dir)
    handle_folder(full_path)
