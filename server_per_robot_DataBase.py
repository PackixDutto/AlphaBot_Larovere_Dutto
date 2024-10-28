import sqlite3
import socket
from pynput import keyboard

# ndirizzo del server e dimensione del buffer
SERVER_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096

#Dizionario per lo stato dei tasti
diz = {"w": False, "a": False, "s": False, "d": False}

#Connessione al database
conn = sqlite3.connect('mio_database.db')
cur = conn.cursor()

#Funzione per inviare i comandi al server
def send_command(command, value):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(SERVER_ADDRESS)
        message = f"{command}|{value}"
        s.sendall(message.encode())
        response = s.recv(BUFFER_SIZE)
        print(f"Risposta dal server: {response.decode()}")
        s.close()
    except Exception as e:
        print(f"Errore di connessione: {e}")

#Funzione chiamata quando un tasto viene premuto
def on_press(key):
    try:
        if key.char in diz and not diz[key.char]:
            diz[key.char] = True
            send_command(key.char, "start")
        else:
            #Se il tasto non è uno dei classici 'w', 'a', 's', 'd'
            cur.execute('SELECT azione FROM comandi WHERE tasto = ?', (key.char,))
            result = cur.fetchone()

            #Se esiste un'azione associata al tasto nel database, esegui quella azione
            if result:
                azione = result[0]
                print(f"Esegui azione: {azione}")
                send_command("azione_speciale", azione)
            else:
                print("Tasto non mappato nel database.")
    except AttributeError:
        pass

#Funzione chiamata quando un tasto viene rilasciato
def on_release(key):
    try:
        if key.char in diz and diz[key.char]:
            diz[key.char] = False
            send_command(key.char, "stop")
    except AttributeError:
        pass

#Funzione per avviare il listener della tastiera
def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

#Funzione principale
def main():
    start_listener()

if __name__ == "__main__":
    main()
    conn.close()
