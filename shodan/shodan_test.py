from shodan import Shodan
import os
from dotenv import load_dotenv
import json
import sys
# Load environmental variables
load_dotenv()
API_KEY = os.getenv("SHODAN_API_KEY")

# Create a Shodan instance
api = Shodan(API_KEY)


# Get the first argument
sysarg = None
if len(sys.argv) > 1:
    sysarg = sys.argv[1]
else:
    print('please specify java or bedrock')
    sys.exit()

# Assign the port based on the argument
version = None
if sysarg == "java":
    port = 25565
    version = "1.21"
elif sysarg == "bedrock":
    port = 19132
    version = "1.21.20"
else:
    print('please specify java or bedrock')
    sys.exit()

# Search for servers
result = api.search(f'product:Minecraft port:{port} version:{version}', limit=500) # limit to 500 to not exhaust credits


bedrock_servers = []

for match in result['matches']:
    entry = {}
    entry['ip'] = match['ip_str']
    entry['version'] = match['minecraft']['version']['name']
    location = {}
    location['country_code'] = match['location']['country_code']
    location['city'] = match['location']['city']
    location['longitude'] = match['location']['longitude']
    location['latitude'] = match['location']['latitude']
    entry['location'] = location
    bedrock_servers.append(entry)

with open(f'shodan_{sysarg}_servers.json', 'w') as f:
    json.dump(bedrock_servers, f, indent=4)