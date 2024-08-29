import socket
import minestat
import sys
import threading
import random
from concurrent.futures import ThreadPoolExecutor


file_lock = threading.Lock()

def check_ip(ip):
    ms = minestat.MineStat(ip, 25565, timeout=8)
    if ms.online:
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        with file_lock:
            with open('working_servers.txt', 'a') as file:
                file.write(f'{ms.address},{ms.port},version: {ms.version},players: {ms.current_players}/{ms.max_players},gamemode: {ms.gamemode},motd: {ms.motd}\n')
                # print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        return True
    
    ms = minestat.MineStat(ip, 19132, timeout=8)
    if ms.online:
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        with file_lock:
            with open('working_servers.txt', 'a') as file:
                file.write(f'{ms.address},{ms.port},version: {ms.version},players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode},motd: {ms.motd}\n')
                # print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        return True
    

    print(f'{ms.address} is offline')
    return False
        


def process_file(file_path, max_threads=40):
    with open(file_path, 'r') as file:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for line in file:
                if line.startswith('open tcp'):
                    ip_address = line.split()[3]
                    executor.submit(check_ip, ip_address)



def main():
    batch_scan_dir = 'batch_scan/112.0.0.0-112.31.185.255'
    ip_range = '112.7.161.32-112.15.66.63'
    max_threads = 100
    process_file(f'{batch_scan_dir}/scan-{ip_range}.txt', max_threads)



main()

print('done')


