import sqlite3
from datetime import datetime, timedelta
import sys
import minestat
from concurrent.futures import ThreadPoolExecutor

# intialize the online_servers and online_with_active_players tables.
# online_servers are servers that return a reply when pinged
# online_with_active_players are servers that return a reply when pinged and have at least one player online
def initialize_tables():
    conn = sqlite3.connect('scan_db.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS online_servers (
            ip_address TEXT NOT NULL,
            port INTEGER NOT NULL,
            version TEXT,
            players TEXT,
            gamemode TEXT,
            motd TEXT,
            latency INTEGER,
            country_code TEXT,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (ip_address, port)
        );
    """
    )

    conn.commit()

    # player_list needed to see who is in the server
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS online_with_active_players (
            ip_address TEXT NOT NULL,
            port INTEGER NOT NULL,
            version TEXT,
            players TEXT,
            player_list TEXT,
            gamemode TEXT,
            motd TEXT,
            latency INTEGER,
            country_code TEXT,
            last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (ip_address, port)
        );
    """
    )

    conn.commit()
    conn.close()

# get the scan results within a certain country
def get_scan_results_w_country_code(db_path, country_code):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scan_results WHERE country_code = ?", (country_code))
    rows = cursor.fetchall()

    conn.close()
    return rows

# fetch all scan results, regardless of country
def get_all_scan_results(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scan_results")
    rows = cursor.fetchall()

    conn.close()
    return rows


def check_sever(scan):
    id, ip_address, port, country_code, date = scan
    try:
        ms = minestat.MineStat(ip_address, port, timeout=5)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    if ms.online:
        # print(f"Server is online!")
        print(f'{ms.address}:{ms.port} is online, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}, country code: {country_code}')
        # add to online_servers table 
        add_server_to_db(ip_address, port, ms.version, f"{ms.current_players}/{ms.max_players}", ms.gamemode, ms.motd, ms.latency, country_code)

        # check if the server has active players
        if ms.current_players > 0:
            # add to online_with_active_players table
            print(f'{ms.address}:{ms.port} has active players, version: {ms.version}, players: {ms.current_players}/{ms.max_players}, gamemode: {ms.gamemode}, motd: {ms.motd}, \n player list:{ms.player_list}, latency: {ms.latency}, country code: {country_code}')
            add_to_online_with_active_players(ip_address, port, ms.version, f"{ms.current_players}/{ms.max_players}", ms.player_list, ms.gamemode, ms.motd, ms.latency, country_code)
    else:
        # print(f"{ip_address}:{port} is offline")
        pass



# adds an online server with active players to the online_with_active_players table
# if an entry already exists, it will be updated
def add_to_online_with_active_players(ip_address, port, version, players, player_list, gamemode, motd, latency, country_code):
    conn = sqlite3.connect('scan_db.db')
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # cursor.execute("INSERT OR REPLACE INTO online_with_active_players (ip_address, port, version, players, gamemode, motd, country_code, last_checked) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ip_address, port, version, players, gamemode, motd, country_code, current_time))
    cursor.execute("""
        INSERT INTO online_with_active_players (ip_address, port, version, players, player_list, gamemode, motd, latency, country_code, last_checked)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (ip_address, port)
        DO UPDATE SET
            version = excluded.version,
            players = excluded.players,
            player_list = excluded.player_list,
            gamemode = excluded.gamemode,
            motd = excluded.motd,
            latency = excluded.latency,
            country_code = excluded.country_code,
            last_checked = excluded.last_checked;
    """, (ip_address, port, version, players, ",".join(player_list), gamemode, motd, latency, country_code, current_time)
    )
    conn.commit()
    conn.close()
    print(f"{ip_address}:{port} added to online_with_active_players table")


def remove_old_entries_from_active():
    conn = sqlite3.connect('scan_db.db')
    cursor = conn.cursor()
    cutoff_time = (datetime.now() - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        DELETE FROM online_with_active_players
        WHERE last_checked < ?
    """, (cutoff_time,)
    )
    conn.commit()
    conn.close()
    print("Old entries removed from online_with_active_players table")


# adds an online server to the online_servers table
def add_server_to_db(ip_address, port, version, players, gamemode, motd, latency, country_code):
    conn = sqlite3.connect('scan_db.db')
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # will insert a new entry or update an existing entry
    cursor.execute("""
        INSERT INTO online_servers (ip_address, port, version, players, gamemode, motd, latency, country_code, last_checked)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (ip_address, port)
        DO UPDATE SET
            version = excluded.version,
            players = excluded.players,
            gamemode = excluded.gamemode,
            motd = excluded.motd,
            latency = excluded.latency,
            country_code = excluded.country_code,
            last_checked = excluded.last_checked;
    """, (ip_address, port, version, players, gamemode, motd, latency, country_code, current_time)
    )
    conn.commit()
    conn.close()
    print(f"{ip_address}:{port} added to online_servers table")

def main(country_code, max_threads):
    initialize_tables()
    country_code = country_code.upper()
    scan_results = None
    if country_code == 'ALL':
        scan_results = get_all_scan_results('scan_db.db')
    else:
        scan_results = get_scan_results_w_country_code('scan_db.db', country_code)

    print(f"found {len(scan_results)} results for {country_code}")

    with ThreadPoolExecutor(max_threads) as executor:
        executor.map(check_sever, scan_results)

    remove_old_entries_from_active()
    print("Status check complete")



max_threads = 500
country_code = 'ALL'
if len(sys.argv) == 3:
    max_threads = sys.argv[1]
    country_code = sys.argv[2]
elif len(sys.argv) == 2:
    max_threads = sys.argv[1]
else:
    print("Using default values for max_threads and country_code")

main(country_code, max_threads)
