import minestat
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import csv
import pandas as pd
import ipaddress
import datetime
from datetime import timezone
import os


online_servers_lock = threading.Lock()

active_players_lock = threading.Lock()

active_servers = []
with open('active_servers.json', 'r') as file:
        try:
            active_servers = json.load(file)
        except json.JSONDecodeError:
            active_servers = []
        
active_with_players_online = []
with open('active_with_players_online.json', 'r') as file:
    try:
        active_with_players_online = json.load(file)
    except json.JSONDecodeError:
        active_with_players_online = []

# time = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def get_ip_range_df():
    df = None
    with open('IP2LOCATION-LITE-DB1.csv', 'r') as f:
        # Create a CSV reader
        reader = csv.reader(f)
        
        df = pd.DataFrame(reader)

        # Rename the columns
        df.columns = ['start', 'end', 'code', 'name']


        # convert the start and end columns to integers
        df['start'] = df['start'].astype(int)
        df['end'] = df['end'].astype(int)

    return df


ip_ranges = get_ip_range_df()

# def check_ip(ip):
#     ms = minestat.MineStat(ip, 25565, timeout=5)
#     if ms.online:
#         print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
#         with file_lock:
#             with open('working_servers.txt', 'a') as file:
#                 file.write(f'{ms.address},{ms.port},version: {ms.version},players: {ms.current_players}/{ms.max_players},gamemode: {ms.gamemode},motd: {ms.motd}\n')
#                 # print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
#         return True
    
#     ms = minestat.MineStat(ip, 19132, timeout=5)
#     if ms.online:
#         print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
#         with file_lock:
#             with open('working_servers.txt', 'a') as file:
#                 file.write(f'{ms.address},{ms.port},version: {ms.version},players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode},motd: {ms.motd}\n')
#                 # print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
#         return True
    

#     print(f'{ms.address} is offline')
#     return False


# def check_ip(ip, port):
#     try:
#         ms = minestat.MineStat(ip, int(port), timeout=5)
#     except Exception as e:
#         print(f'Error: {e}')
#         return
#     if ms.online:
#         # temporary solution: get country code by range
#         ip_decimal = int(ipaddress.ip_address(ip))
#         country_code = ip_ranges[(ip_decimal >= ip_ranges['start']) & (ip_decimal <= ip_ranges['end'])]['code'].values[0]
#         print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}, country code: {country_code}')
#         # get current date and time
#         with online_servers_lock:
#             with open('working_servers.json', 'r+') as file:
#                 print('inside active_servers.json')
#                 current_ips = json.load(file)
#                 print('current ips: ', current_ips)
#                 # time = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
#                 print(time)
#                 for entry in current_ips:
#                     if entry['address'] == ip:
#                         entry['version'] = ms.version # server versions may change
#                         entry['players'] = f'{ms.current_players}/{ms.max_players}' # player count may change
#                         entry['gamemode'] = ms.gamemode # gamemode may change as well
#                         entry['motd'] = ms.motd # motd may change
#                         entry['lasted_checked'] = time # update last time checked
#                         break
#                 else:
#                     current_ips.append({
#                         'address': ms.address,
#                         'port': ms.port,
#                         'version': ms.version,
#                         'players': f'{ms.current_players}/{ms.max_players}',
#                         'gamemode': ms.gamemode,
#                         'motd': ms.motd,
#                         'country_code': country_code,
#                         'lasted_checked': time
#                     })
                    
#                 file.seek(0)
#                 json.dump(current_ips, file, indent=4)
#                 file.truncate()
#         # check if player count > 0
#         if ms.current_players > 0:
#             with active_players_lock:
#                 with open('active_with_players_online.json', 'r+') as file:
#                     current_ips = json.load(file)
#                     # time = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
#                     for entry in current_ips:
#                         if entry['address'] == ip:
#                             entry['version'] = ms.version # server versions may change
#                             entry['players'] = f'{ms.current_players}/{ms.max_players}' # player count may change
#                             entry['gamemode'] = ms.gamemode # gamemode may change as well
#                             entry['motd'] = ms.motd # motd may change
#                             entry['lasted_checked'] = time # update last time checked
#                         else:
#                             current_ips.append({
#                                 'address': ms.address,
#                                 'port': ms.port,
#                                 'version': ms.version,
#                                 'players': f'{ms.current_players}/{ms.max_players}',
#                                 'gamemode': ms.gamemode,
#                                 'motd': ms.motd,
#                                 'country_code': country_code,
#                                 'lasted_checked': time
#                             })
#                     file.seek(0)
#                     json.dump(current_ips, file, indent=4)
#                     file.truncate()
#         return
        
#     print(f'{ms.address} is offline')
#     return


def check_ip(ip, port):
    try:
        ms = minestat.MineStat(ip, int(port), timeout=5)
    except Exception as e:
        print(f'Error: {e}')
        return
    if ms.online:
        # temporary solution: get country code by range
        ip_decimal = int(ipaddress.ip_address(ip))
        country_code = ip_ranges[(ip_decimal >= ip_ranges['start']) & (ip_decimal <= ip_ranges['end'])]['code'].values[0]
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}, country code: {country_code}')
        # get current date and time
        with online_servers_lock:
            print('current ips: ', active_servers)
            time = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            for entry in active_servers:
                if entry['address'] == ip:
                    entry['version'] = ms.version # server versions may change
                    entry['players'] = f'{ms.current_players}/{ms.max_players}' # player count may change
                    entry['gamemode'] = ms.gamemode # gamemode may change as well
                    entry['motd'] = ms.motd # motd may change
                    entry['lasted_checked'] = time # update last time checked
                    break
            else:
                active_servers.append({
                    'address': ms.address,
                    'port': ms.port,
                    'version': ms.version,
                    'players': f'{ms.current_players}/{ms.max_players}',
                    'gamemode': ms.gamemode,
                    'motd': ms.motd,
                    'country_code': country_code,
                    'lasted_checked': time
                })
        # check if player count > 0
        if ms.current_players > 0:
            with active_players_lock:
                time = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                for entry in active_with_players_online:
                    if entry['address'] == ip:
                        entry['version'] = ms.version # server versions may change
                        entry['players'] = f'{ms.current_players}/{ms.max_players}' # player count may change
                        entry['gamemode'] = ms.gamemode # gamemode may change as well
                        entry['motd'] = ms.motd # motd may change
                        entry['lasted_checked'] = time # update last time checked
                else:
                    active_with_players_online.append({
                        'address': ms.address,
                        'port': ms.port,
                        'version': ms.version,
                        'players': f'{ms.current_players}/{ms.max_players}',
                        'gamemode': ms.gamemode,
                        'motd': ms.motd,
                        'country_code': country_code,
                        'lasted_checked': time
                    })
        # print('active servers: ', active_servers)
        return
        
    print(f'{ms.address} is offline')
    return

# def process_file(file_path, max_threads=40):
#     with open(file_path, 'r') as file:
#         with ThreadPoolExecutor(max_workers=max_threads) as executor:
#             for line in file:
#                 if line.startswith('open tcp'):
#                     ip_address = line.split()[3]
#                     executor.submit(check_ip, ip_address)




def process_file(file_path, max_threads=40):
    with open(file_path, 'r') as file:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for line in file:
                if line.strip():
                    info = line.split(' ')
                    ip_address = info[0]
                    port = info[1]
                    executor.submit(check_ip, ip_address, port)


def main():
    if not os.path.exists('active_servers.json'):
        # Create an empty list and write it to the file
        with open('active_servers.json', 'w') as file:
            json.dump([], file)

    if not os.path.exists('active_with_players_online.json'):
        with open('active_with_players_online.json', 'w') as file:
            json.dump([], file)

    max_threads = 1000
    process_file('merged_ips.txt', max_threads)

    with open('active_servers.json', 'w') as file:
        json.dump(active_servers, file, indent=4)

    with open('active_with_players_online.json', 'w') as file:
        json.dump(active_with_players_online, file, indent=4)


main()

print('done')


