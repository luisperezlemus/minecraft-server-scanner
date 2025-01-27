# Before you begin
You must download the IP2LOCATION csv file: https://lite.ip2location.com/download?id=1. Move the csv file into this project's directory. Rename scanned_ranges_example.csv to scanned_ranges.csv. I made it empty to exclude my file that I have stored locally.

# Select your country and IP size range
Begin by running `get_ip_ranges.py`. First, pass in the two letter country code. Then the minimum number of hosts and 
maximum number of hosts per IP block. Some IP blocks are very small and slow down the scanning, so these 
parameters give us the option to focus on whatever size ranges you want to scan. 

Example: `python get_ip_ranges.py US 5624575 33566719`

This will create a directory named ip_ranges and inside will be a text file named ip-ranges-<country_code>.txt.
This contains the ip blocks/ranges that we will be scanning.

To help visualize the ip ranges, you can can run `filter_ips.py` to see the ip blocks per country.

Example usage: `python filter_ips.py US`

# Scanning the IP blocks/ranges
Run `scan.py` to scan the IP blocks/ranges. This will take the longest. The temp directory is created to track the scanning
progress. Once the scanning is complete, the temporary folders will be deleted and the scan results are stored in the scan_db.db database in the scan_results table. 

Usage: `python scan.py <country_code> <ports> <rate> <batch_size>`<br />
Example usage: `python scan.py US 19132,25565 5000 1000000`

# Verify Minecraft server status
Not all ip addresses in the scan results will be Minecraft servers. Minecraft has their own server protocol, so I use the `minestat` Python library to verify which ip addresses are legitimate servers. Run `mc_status_check.py`. Arguments are optional. The default is max_threads = 1000 and country_code = ALL. ALL meaning the country does not matter, we scan all ip addresses in scan_results. If you want to pass arguments, you must specify the number of threads first then the country.

Usage: `python mc_status_check.py <max_threads> <country_code>` <br />
or `python mc_status_check.py <max_threads>` 

After this completes, new tables in scan_db.db will be created: online_servers and online_with_active_players. online_servers are servers that are online. online_with_active_players are servers that currently have players in them.


# Future Plans
I have plans to create an application to display the online servers and servers with players in them, but for now the servers are in the SQLite database, so basic knowledge of SQL is required to view the data.