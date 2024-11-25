import sqlite3
import socket

# Impostazioni server
MY_ADDRESS = ("127.0.0.1", 9090)
NETWORK = "192.168.0.0/27"
BUFFER_SIZE = 4096
COMMON_PORTS = [22, 80, 443, 21, 25, 53, 110, 143, 3306, 3389]

def scansione_host():
    open_ports = []
    try:
        host_name = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host_name = None

    for port in COMMON_PORTS:
        sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

def scansione_network():
    threads=[]
    for ip in ip_network(NETWORK).hosts():
        thread = threading.Thread(target=scan_host, args=(str(ip),))
        threads.append(thread)

    for thread in threads:
        thread.join()

def createdatabase():
    conn = sqlite3.connect("ip_list.db")
    cur = conn.cursor()

    query = """CREATE TABLE IF NOT EXIST host(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_host INTAGER,
                nome_host VARCHAR(20)
                port_list INTAGER
                )"""
    cur.execute(query)
    cur.execute("INSERT INTO ip_list(ip_host, nome_host, port_list) VALUES (?, ?, ?)",
                (ip, host_name.ù, ','.join(map(str, open_port))))
    conn.commit()
    conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    while True:
        connection, client_address = s.accept()
        print(f"Il client {client_address} si è connesso")


if __name__ == "__main__":
    main()


