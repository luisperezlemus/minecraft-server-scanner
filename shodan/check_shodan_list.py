import minestat
import sys
import threading
import random
import json



def read_json(file):
    with open(file, 'r') as f:
        return json.load(f)


def check_ip(ip, port):
    ms = minestat.MineStat(ip, port, timeout=0.5)
    if ms.online:
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        return True
    else:
        return False
    
def check_server_ip(server):
    ip = server['ip']
    ms = minestat.MineStat(ip, 25565, timeout=0.5)
    if ms.online:
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        return {
            'ip': ip,
            'port': 25565,
            'version': ms.version,
            'players': f"{ms.current_players} / {ms.max_players}",
            'gamemode': ms.gamemode, 
            'motd': ms.motd,
            'player_list': ms.player_list,
            'latency': ms.latency
        }
    else:
        return False
        
def check_players_online(ip, port):
    ms = minestat.MineStat(ip, port, timeout=0.5)
    if ms.online and ms.current_players > 0:
        print(f'{ms.address}:{ms.port} has players online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        return {
            'ip': ip,
            'port': port,
            'version': ms.version,
            'players': f"{ms.current_players} / {ms.max_players}",
            'gamemode': ms.gamemode, 
            'motd': ms.motd,
            'player_list': ms.player_list,
            'latency': ms.latency
        }
    else:
        return False
    
def check_players_online_server(server):
    ip = server['ip']
    res = check_players_online(ip, 25565)
    if res != False:
        return {
            'ip': ip,
            'port': 25565,
            'version': res['version'],
            'players': res['players'],
            'gamemode': res['gamemode'],
            'motd': res['motd'],
            'player_list': res['player_list'],
            'latency': res['latency'],
            'country': server['location']['country_code'],
            'city': server['location']['city'],
        }
    else:
        return False

# # Create 20 threads
# threads = []
# for i in range(1, 21):
#     start_octets = [(i-1) * 256**3, 0, 0, 0]
#     end_octets = [i * 256**3 - 1, 255, 255, 255]
#     thread = threading.Thread(target=scan_ip_range, args=(start_octets, end_octets))
#     threads.append(thread)
#     thread.start()

# # Wait for all threads to finish
# for thread in threads:
#     thread.join()

# data = read_json('shodan_bedrock_servers.json')
data = read_json('shodan_java_servers.json')
online_w_players_servers = []
online_servers = []
for server in data:
    ip = server['ip']
    # online = check_ip(ip, 25565)
    online = check_server_ip(server)
    if online:
        online_servers.append(server)
        res_w_players = check_players_online_server(server)
        if res_w_players != False:
            online_w_players_servers.append(res_w_players)

with open('java_servers_w_players.json', 'w') as f:
    json.dump(online_w_players_servers, f, indent=4)

with open('java_servers_online.json', 'w') as f:
    json.dump(online_servers, f, indent=4)