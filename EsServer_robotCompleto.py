import socket
import RPi.GPIO as GPIO
import time
import AlphaBot
import sqlite3
import threading

#Indirizzo del server e dimensione del buffer
MY_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
DATABASE = "mio_database.db"

alice = AlphaBot.AlphaBot()
alice.stop()

#Comandi disponibili per il robot
commands = {"forward": alice.backward, "backward": alice.forward, "left": alice.left, "right": alice.right}

def client_handler(client_socket, alice):
    #Parte database
    conn = sqlite3.connect(DATABASE)  #Mi creo la connessione al database
    cur = conn.cursor()  # i creo il cursore con cui vado ad operare il database
    client_socket.settimeout(6)  #Timeout di 6 secondi per il client

    try:  #Aspetto 6 secondi sennò chiudo il client
        #Parte Messaggio
        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE)  # Prendo il messaggio
                if not message:  #Il client si è chiuso
                    break

                string = message.decode().split("|")  #Decodifica del messaggio ricevuto
                if len(string) == 2:
                    command = string[0]
                    value = string[1]
                    print(f"Comando ricevuto: {command} con valore {value}")

                    # e valido il comando, eseguo
                    if command in commands:
                        if value == "start":  #Inizia a muoversi
                            commands[command]()  #Esegue la funzione associata al comando
                            response = f"ok|Comando {command} iniziato"
                        elif value == "stop":  #Ferma il movimento
                            alice.stop()
                            response = f"ok|Comando {command} fermato"
                        else:
                            response = "error|Valore non valido"
                    else:
                        response = "error|Comando non riconosciuto"
                else:
                    print("PASSA QUA UN SINGOLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOo")
                    command = string[0]  #Tasto
                    query = f'''SELECT azione
                        FROM comandi
                        WHERE tasto = {command}'''
                    cur.execute(query)
                    result = cur.fetchone()  #Mi prendo il risultato
                    if result:  #Se esiste (è nel database)
                        azione = result[0]
                        print(f"Azione trovata per il tasto {command}: {azione}")
                        #Fare l'azione
                        response = f"ok|Azione: {azione}"
                    else:
                        response = "error|Tasto non trovato nel database"

                #Invio della risposta al client
                client_socket.send(response.encode())

            except socket.timeout:
                print("FERMA TUTTO: Timeout raggiunto.")
                alice.stop()
                client_socket.close()
                break

    finally:
        conn.close()
        client_socket.close()

def createDatabase():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    #Se non esiste la tabella
    cur.execute('''
        CREATE TABLE IF NOT EXISTS comandi (
            tasto VARCHAR(1) PRIMARY KEY,
            azione TEXT
        )''')
    conn.commit()
    conn.close()

def main():
    createDatabase()  #Creo il database se non esiste
    #Creazione del socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(MY_ADDRESS)
    server_socket.listen()

    print("Server in ascolto su", MY_ADDRESS)

    while True:  #Sono alla ricerca di client
        client_socket, client_address = server_socket.accept()  #Accetto il client
        print(f"Connessione stabilita con {client_address}")

        client_handler_thread = threading.Thread(target=client_handler, args=(client_socket, alice))  #Mi gestisco i vari client con il threading
        client_handler_thread.start()

if __name__ == "__main__":
    main()
