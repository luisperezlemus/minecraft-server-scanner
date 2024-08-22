import socket
import minestat
import sys
import threading
import random
from concurrent.futures import ThreadPoolExecutor


file_lock = threading.Lock()

def check_ip(ip, port):
    ms = minestat.MineStat(ip, port, timeout=8)
    if ms.online:
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        with file_lock:
            with open('working_servers.txt', 'a') as file:
                file.write(f'{ms.address},{ms.port}, version: {ms.version}, players: {ms.current_players}/{ms.max_players}\n')
                # print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}')
        return True
    else:
        print(f'{ms.address}:{ms.port} is offline')
        return False
        


def process_file(file_path, max_threads=20):
    with open(file_path, 'r') as file:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            for line in file:
                if line.startswith('open tcp'):
                    ip_address = line.split()[3]
                    executor.submit(check_ip, ip_address, 19132)



def main():
    ip_range = '75.0.0.0-76.0.0.0'
    max_threads = 20
    process_file(f'scan-{ip_range}.txt', max_threads)



main()

print('done')


