import os

# directory were the scanning results are stored
batch_scan_path = 'batch_scan'

output_file_path = 'merged_ips.txt'

with open(output_file_path, 'w') as output_file:
    # iterate through the folders inside batch_scan 
    for folder_name in os.listdir(batch_scan_path):
        folder_path = os.path.join(batch_scan_path, folder_name)
        
        # verify that it's a directory
        if os.path.isdir(folder_path):
            # iterate through the files inside the folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                # verify that it's a file
                if os.path.isfile(file_path):
                    with open(file_path, 'r') as input_file:
                        for line in input_file:
                            # check that line is not empty or isn't a comment
                            if line.strip() and not line.startswith('#'):
                                split = line.split()
                                port, ip = split[2], split[3] # example of the masscan format: open tcp 19132 1.72.51.252 1724782731
                                output_file.write(f"{ip} {port}\n")