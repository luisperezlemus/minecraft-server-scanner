Begin by running get_ip_ranges.py. First, pass in the country you get to scan, then the minimum number of hosts and 
maximum number of hosts per IP block. Some IP blocks are very small and slow down the scanning, so these 
parameters give us the option to focus on whatever size ranges you want to scan.

Then run scan.py to scan the IP blocks/ranges. This will take the longest. Once the scanning is complete
the temporary folders will be deleted and the scan results are stored in the scan_db.db database in the scan_results
table.