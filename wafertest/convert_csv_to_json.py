import csv
import json 
import custom_filehandler as cfile

json_data = []


files = cfile.get_all_filenames_in_folder(startdir="IV_Die_1/Subdie_1_ADiodes_4", file_extension=".csv")

for file in files:
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            json_data.append(row)

dump = json.dumps(json_data, indent=4)

with open("json/dump.json", mode="w", encoding="utf-8") as write_file:
    json.dump(json_data, write_file, sort_keys=True, indent=4)