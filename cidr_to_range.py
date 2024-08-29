import ipaddress

with open('major_isps.txt', 'r') as file:
    lines = file.readlines()

with open('major_isps.txt', 'w') as file:
    for line in lines:
        # Check if the line contains a CIDR notation
        if '/' in line:
            # Split the line into IP address and prefix length
            ip, prefix_length = line.strip().split('/')
            
            # Convert the CIDR notation to an IP network object
            network = ipaddress.ip_network(line.strip())
            
            # Get the IP range from the network object
            ip_range = f"{network.network_address}-{network.broadcast_address}"
            
            # Replace the line with the IP range
            line = ip_range + '\n'
        
        # Write the line to the output file
        file.write(line)