# after selecting the country you want, and the parameters for the ip block sizes, this script will
# read the ip-ranges-{country_code}.txt file in the ip_ranges folder split the ip ranges into batches
# based on batch_size, then run the scanner for each batch. The results will be stored in temp/{country_code}/results.txt
# once all the ip_ranges have been scanned, the results will be stored in a sqlite database and the temp folder will be deleted
# the table that stores this information is named scan_results

import os
import subprocess
import sys
import pickle
from datetime import datetime
import csv

# convert ip x.x.x.x to integer
def ip_to_int(ip):
    a, b, c, d = map(int, ip.split('.'))
    return (a << 24) + (b << 16) + (c << 8) + d

# convert integer to ip x.x.x.x
def int_to_ip(ip_int):
    return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"

# now we know the batches text file exists, now read through each line and run the scanner
def run_scanner(ip_range, ports, rate, country_code):
    try:
        command = [
            'sudo', 'masscan',
            ip_range,
            f'-p{ports}',
            '--rate', rate,
            '--excludefile', 'exclude.conf',
            '-oL', f'temp/{country_code}/scan.txt',
            '--wait', '3',
            '--open-only'
        ]
        # the script already writes the results, so no need to code anything here
        # sudo masscan $START_IP-$END_IP -p$PORTS --rate $RATE --excludefile exclude.conf -oL temp/$COUNTRY_CODE/scan.txt --wait 3 --open-only
        subprocess.run(command, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.output)

# all we need is to run the scanner per batch
def process_batches(ip_block, file_path, ports, rate, country_code):
    # we calculate the number of responses by getting the number of lines in the results.txt file before batch scanning
    # then we get the number of lines after batch scanning and subtract the two to get the number of responses
    global_state = {}
    with open(f"temp/{country_code}/global_state.pkl", "rb") as f:
            global_state = pickle.load(f)
    while True:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            print("All batches have been scanned")
            break

        ip_range = lines[0].strip()
        print("first line of the text file: ", ip_range)

        run_scanner(ip_range, ports, rate, country_code)

        with open(file_path, 'w') as f:
            f.writelines(lines[1:]) # remove the first line after it's been processed

        output = ""
        if os.path.exists(f"temp/{country_code}/scan.txt"):
            with open(f"temp/{country_code}/scan.txt", "r") as f:
                output = f.readlines()
                print(f"found {len(output)} hosts in this batch")
                if len(output) > 0:
                    output = output[1:-1]
                else:
                    output = ""
    
        if output != "":
            results_file = f"temp/{country_code}/results.txt"
            if not os.path.exists(results_file):
                with open(results_file, "w") as f:
                    pass
            with open(results_file, "a") as f:
                f.writelines(output)
            global_state[ip_block] += len(output)
        if os.path.exists(f"temp/{country_code}/scan.txt"):
            os.remove(f"temp/{country_code}/scan.txt")


    # delete batches.txt after each range is complete
    if os.path.exists(file_path):
        os.remove(file_path)
    print("batches file deleted")
    response_count = global_state[ip_block]
    del global_state[ip_block]
    return response_count
        
def scan_ranges(ports, rate, batch_size, country_code):
    # we will read the ip-ranges-{country_code}.txt file for each ip range, then we will creaate batches for each ip range
    # then we will scan the range, once the range is complete, we remove it from the text file and move on to the next line
    while True:
        if os.path.exists(f"temp/{country_code}/batches.txt"):
            print("batches file exists")
            with open(f"ip_ranges/ip-ranges-{country_code.upper()}.txt", 'r') as f:
                lines = f.readlines()
            ip_block = lines[0].strip()
            response_count = process_batches(ip_block, f"temp/{country_code}/batches.txt", ports, rate, country_code)

            with open(f"ip_ranges/ip-ranges-{country_code.upper()}.txt", 'r') as f:
                lines = f.readlines()
                
            if lines:
                ip_range = lines[0].strip()
                # track the scanned ranges
                # with open("scanned_ranges.csv", "a") as csv_file:
                #     csv_file.write(f"{ip_range},\"{ports}\",{country_code},{response_count},{datetime.now()}\n")
                csv_entry = {
                    'ip_range': ip_range,
                    'ports': ports,
                    'country_code': country_code,
                    'responses': response_count,
                    'datetime': datetime.now()
                }
                update_csv("scanned_ranges.csv", csv_entry)

                with open(f"ip_ranges/ip-ranges-{country_code.upper()}.txt", "w") as f:
                    f.writelines(lines[1:])
        else:
            with open(f"ip_ranges/ip-ranges-{country_code.upper()}.txt", "r") as f:
                ip_range = f.readline().strip()
            print(ip_range)

            if not ip_range:
                print("All IP ranges have been scanned")
                break

            # create a temporary folder only if it doesn't already exist
            temp_folder = f"temp/{country_code}"
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # calculate batches
            batches_file = f"{temp_folder}/batches.txt"
            if not os.path.exists(batches_file):
                start_ip = ip_range.split("-")[0]
                end_ip = ip_range.split("-")[1]

                # print('start ip:', start_ip)
                # print('end ip: ', end_ip)

                start_ip_int = ip_to_int(start_ip)
                end_ip_int = ip_to_int(end_ip)

                # print(f"start ip int to ipv4: {int_to_ip(start_ip_int)}")
                # print(f"end ip int to ipv4: {int_to_ip(end_ip_int)}")

                batch_size = int(batch_size)
                batches = []

                for ip_int in range(start_ip_int, end_ip_int + 1, batch_size):
                    batch_end_ip_int = min(ip_int + batch_size - 1, end_ip_int) # ensures not to go over the end ip
                    batches.append((ip_int, batch_end_ip_int))

                with open(f"{temp_folder}/batches.txt", "w") as batch_file:
                    for i, (start, end) in enumerate(batches):
                        if i == len(batches) - 1:
                            batch_file.write(f"{int_to_ip(start)}-{int_to_ip(end)}")
                        else:
                            batch_file.write(f"{int_to_ip(start)}-{int_to_ip(end)}\n")
                        
                print(f"split into {len(batches)} batches")

            global_state = {}
            if not os.path.exists(f"temp/{country_code}/global_state.pkl"):
                global_state = {
                    ip_range: 0
                }
                with open(f"temp/{country_code}/global_state.pkl", "wb") as f:
                    pickle.dump(global_state, f)
            else:
                with open(f"temp/{country_code}/global_state.pkl", "rb") as f:
                    global_state = pickle.load(f)
                if ip_range not in global_state:
                    global_state[ip_range] = 0
                    with open(f"temp/{country_code}/global_state.pkl", "wb") as f:
                        pickle.dump(global_state, f)

            file_path = f"{temp_folder}/batches.txt"
            # don't need to pass the ip_range since they're already split into batches
            # ip_range is the whole ip block here
            response_count = process_batches(ip_range, file_path, ports, rate, country_code)
            # track the scanned ranges
            # with open("scanned_ranges.csv", "a") as csv_file:
            #     csv_file.write(f"{ip_range},\"{ports}\",{country_code},{response_count},{datetime.now()}\n")
            csv_entry = {
                'ip_range': ip_range,
                'ports': ports,
                'country_code': country_code,
                'responses': response_count,
                'datetime': datetime.now()
            }
            update_csv("scanned_ranges.csv", csv_entry)
            # delete the ip range after the batches have been scanned
            with open(f"ip_ranges/ip-ranges-{country_code.upper()}.txt", 'r') as f:
                lines = f.readlines()

            if lines:
                with open(f"ip_ranges/ip-ranges-{country_code.upper()}.txt", "w") as f:
                    f.writelines(lines[1:])

# update the csv file that tracks the ranges that have been scanned
# this might be really slow once scanned_ranges.csv gets large, not sure yet
def update_csv(file_path, new_entry):
    temp_file = file_path + ".tmp"
    entry_updated = False

    with open(file_path, "r") as f, open(temp_file, "w", newline='') as t:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(t, fieldnames)
        writer.writeheader()

        for row in reader:
            if row['ip_range'] == new_entry['ip_range']:
                writer.writerow(new_entry)  # update the entry
                entry_updated = True
            else:
                writer.writerow(row) # write the existing entry
        if not entry_updated: # if the entry doesn't exist, add it
            writer.writerow(new_entry)

    os.replace(temp_file, file_path)

# get command line arguments
if len(sys.argv) < 5:
    print("Usage: python scan.py <country_code> <ports> <rate> <batch_size>")
    sys.exit(1)

country_code = sys.argv[1]
ports = sys.argv[2]
rate = sys.argv[3]
batch_size = sys.argv[4]

# begin scanning
scan_ranges(ports, rate, batch_size, country_code)
print("Scanning complete, saving to database...")

import sqlite3
import shutil

# create a table to store the scanning results
def initialize_results_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            port INTEGER NOT NULL,
            country_code TEXT NOT NULL,
            datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP          
        )
    """
    )
    conn.commit()
    conn.close()

# creates an entry in the scan_results table
def insert_result(db_path, ip_address, port, country_code):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO scan_results (ip_address, port, country_code, datetime) VALUES (?, ?, ?, ?)
    """, (ip_address, port, country_code, current_time))
    conn.commit()
    conn.close()

def process_and_store_results(results_path, db_path, country_code):
    with open(results_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.split()
        if len(parts) == 5 and parts[0] == "open":
            port = int(parts[2])
            ip_address = parts[3]
            insert_result(db_path, ip_address, port, country_code)

def remove_duplicates(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(""" 
        DELETE FROM scan_results
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM scan_results
            GROUP BY ip_address, port)
    """
    )
    conn.commit()
    conn.close()

db_path = "scan_db.db"
results_path = f"temp/{country_code}/results.txt"


if os.path.exists(f"temp/{country_code}/results.txt"):
    initialize_results_db(db_path)
    process_and_store_results(results_path, db_path, country_code)
    remove_duplicates(db_path) 
    
    # TODO: delete the temp folder after the scan is complete and the results are stored in the database
    # remove the temporary directory that was created when scanning
    shutil.rmtree(f"temp/{country_code}")
    # if there are no other countries being scanned, then remove the temp directory as well
    if len(os.listdir("temp")) == 0:
        os.rmdir("temp")

    # remove the ip ranges file located in ip_ranges-<country_code>.txt
    if os.path.exists(f"ip_ranges/ip-ranges-{country_code.upper()}.txt"):
        os.remove(f"ip_ranges/ip-ranges-{country_code.upper()}.txt")
    if len(os.listdir("ip_ranges")) == 0:
        os.rmdir("ip_ranges")

    print("Results saved to database")