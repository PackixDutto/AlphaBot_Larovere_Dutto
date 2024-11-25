import sqlite3

import socket
from pynput import keyboard

# Indirizzo del server e dimensione del buffer
SERVER_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096

# Dizionario per lo stato dei tasti
diz = {"w": False, "a": False, "s": False, "d": False, "u": False}

# Funzione per inviare i comandi al server
def send_command(command, value):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(SERVER_ADDRESS)
        message = f"{command}|{value}"
        if command not in diz:
            s.sendall(f"{command}") #Per inviare solo il comando
        else:
            s.sendall(message.encode())  # Invia il comando ed il value
        response = s.recv(BUFFER_SIZE)
        print(f"Risposta dal server: {response.decode()}")
        s.close()
    except Exception as e:
        print(f"Errore di connessione: {e}")

# Funzione chiamata quando un tasto viene premuto
def on_press(key):
    try:
        if key.char == "w" and not diz["w"]:
            diz["w"] = True
            send_command("forward", "start")
        elif key.char == "a" and not diz["a"]:
            diz["a"] = True
            send_command("left", "start")
        elif key.char == "s" and not diz["s"]:
            diz["s"] = True
            send_command("backward", "start")
        elif key.char == "d" and not diz["d"]:
            diz["d"] = True
            send_command("right", "start")
        elif key.char == "u" and not diz["u"]:
            diz["u"] = True
            send_command("database", "start")
    except AttributeError:
        pass

# Funzione chiamata quando un tasto viene rilasciato
def on_release(key):
    try:
        if key.char == "w" and diz["w"]:
            diz["w"] = False
            send_command("forward", "stop")
        elif key.char == "a" and diz["a"]:
            diz["a"] = False
            send_command("left", "stop")
        elif key.char == "s" and diz["s"]:
            diz["s"] = False
            send_command("backward", "stop")
        elif key.char == "d" and diz["d"]:
            diz["d"] = False
            send_command("right", "stop")
        elif key.char == "u" and not diz["u"]:
            diz["u"] = True
            send_command("u", "database")
        elif key.char == "i" and not diz["u"]:
            diz["i"] = True
            send_command("i", "database")
    except AttributeError:
        pass

# Funzione per avviare il listener della tastiera
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Funzione principale
def main():
    start_listener()

if __name__ == "__main__":
    main()





# Connessione al database (crea il file se non esiste)
conn = sqlite3.connect('mio_database.db')
cur = conn.cursor()

# Creazione della tabella (se non esiste)
# La tabella ha una colonna 'tasto' (PRIMARY KEY) e una 'azione' associata al tasto
cur.execute('''
    CREATE TABLE IF NOT EXISTS comandi (
        tasto VARCHAR(1) PRIMARY KEY,
        azione TEXT
    )
''')

comandi = [
    ('u', 'F100'),  # Avanza di 100
    ('i', 'L40'),   # Gira a sinistra di 40
]


cur.executemany('INSERT OR REPLACE INTO comandi (tasto, azione) VALUES (?, ?)', comandi)
conn.commit()

print("Tabella comandi creata e popolata con successo.")
conn.close()


######bisogna passare questo in client_per_robot in qualche modo 