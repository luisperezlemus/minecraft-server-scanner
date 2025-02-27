import csv
import pandas as pd
import ipaddress
import os
import sys
import sqlite3

if len(sys.argv) < 2:
    print("Please provide the country code")
    sys.exit(1)

# Get the country code from the command line argument
country_code = sys.argv[1]

def show_ip_ranges(country_code):
    with open('IP2LOCATION-LITE-DB1.csv', 'r') as f:
        # Create a CSV reader
        reader = csv.reader(f)
        
        df = pd.DataFrame(reader)

        # Rename the columns
        df.columns = ['start', 'end', 'code', 'name']

        # convert the start and end columns to integers
        df['start'] = df['start'].astype(int)
        df['end'] = df['end'].astype(int)

        # Calculate the difference between end and start columns (number of hosts)
        df['diff'] = df['end'] - df['start']

        # filter by country code
        df = df[df['code'] == country_code]

        # sort the df by the diff column in descending order
        df = df.sort_values('diff', ascending=True) 
        

        # convert decimal to ip address
        df['start'] = df['start'].apply(lambda x: ipaddress.ip_address(x))
        df['end'] = df['end'].apply(lambda x: ipaddress.ip_address(x))

        # sort by difference size, with the biggest being first
        df = df.sort_values('diff', ascending=False)
        print(df)
        # Save the results into a text file
        output_file = 'filtered_ips.txt'
        df.to_csv(output_file, index=False, sep='\t')
        print(f"Results saved to {output_file}")

        # # Filter the entries with diff equal to 32767
        # df_filtered = df[df['diff'] == 32767]

        # # Print the filtered DataFrame
        # print(df_filtered)


def show_scan_results():
    conn = sqlite3.connect('scan_db.db')   
    cursor = conn.cursor()

    # Get the scan results
    cursor.execute("SELECT * FROM scan_results")
    rows = cursor.fetchall()

    # Print the scan results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# show_scan_results()

show_ip_ranges(country_code)