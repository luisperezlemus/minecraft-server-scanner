import csv
import pandas as pd
import ipaddress
import os
import sys

# Get the country code from the command line argument
country_code = sys.argv[1]

# Print the country code for verification
# print(f"Country code: {country_code}")

# Open the CSV file
# link to download: https://lite.ip2location.com/database/ip-country?lang=en_US
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

    # since there's many ip addresses, we filter out the ones with more than 1 million to get higher ranges
    # TODO: pass number of hosts per range as a command line argument
    df = df[df['diff'] > 100000]

    # Read the exclude.conf file because government and military subnets IPs are very large so we don't want to waste time on them
    with open('exclude.conf', 'r') as exclude_file:
        # Read the IP addresses to exclude, ignoring comments that start with #
        exclude_ips = [line.strip() for line in exclude_file if line.strip() and not line.startswith('#')]
        # Remove the CIDR format from exclude_ips, only need the starting IP address
        exclude_ips = [ip.split('/')[0] for ip in exclude_ips]
        # print(exclude_ips)

    # only look for the starting address since that's when the range starts
    df = df[~df['start'].astype(str).isin(exclude_ips)]

    # Navigate through the folders inside the batch_scan folder because we don't want to list the ranges
    # that have already been scanned
    for folder_name in os.listdir('batch_scan'):
        # print(folder_name)
        
        # Split the folder name using the '-'
        start, end = folder_name.split('-')
        # print(start, end)
        
        # filter out the existing ranges to avoid rescanning them
        df = df[(df['start'].astype(str) != start) & (df['end'].astype(str) != end)]

   
    print(df)

    # Create the ip-ranges directory if it doesn't exist
    os.makedirs('ip_ranges', exist_ok=True)
    # Write the IP ranges to a file
    with open(f'ip_ranges/ip-ranges-{country_code}.txt', 'w') as outfile:
        # Loop through each entry in df
        for index, row in df.iterrows():
            start_ip = str(row['start'])
            end_ip = str(row['end'])
            
            # Write the IP range to the file
            outfile.write(f"{start_ip}-{end_ip}\n")
