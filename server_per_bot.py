import socket
import threading
import RPi.GPIO as GPIO
import time
import AlphaBot

# Indirizzo del server e dimensione del buffer
MY_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
alice = AlphaBot.AlphaBot()
alice.stop()

# Variabile di controllo per la perdita dell'heartbeat
heartbeat_lost = False

# Comandi disponibili per il robot
commands = {
    "forward": alice.forward,
    "backward": alice.backward,
    "left": alice.left,
    "right": alice.right,
}

# Funzione per gestire la ricezione degli heartbeat
def hearthbeat_receive(recive_heartbeat):
    global heartbeat_lost
    recive_heartbeat.settimeout(6.5)
    while not heartbeat_lost:
        try:
            data = recive_heartbeat.recv(4096)
            if data:
                print("Heartbeat ricevuto")
            else:
                print("Heartbeat terminato")
                heartbeat_lost = True
        except socket.timeout:
            print("FERMA TUTTO - Timeout Heartbeat")
            heartbeat_lost = True
        except Exception as e:
            print(f"Errore durante la ricezione dell'heartbeat: {e}")
            heartbeat_lost = True

# Funzione principale per gestire i comandi
def main():
    global heartbeat_lost

    # Creazione dei socket per comandi e heartbeat
    socket_command = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_heartbeat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa i socket a un indirizzo e porta
    socket_command.bind(("localhost", 12345))
    socket_heartbeat.bind(("localhost", 12346))

    # Il server ascolta le connessioni in entrata
    socket_command.listen(1)
    socket_heartbeat.listen(1)
    print("Server TCP in attesa di connessioni...")

    # Accetta una connessione per i comandi
    recive_command, address1 = socket_command.accept()
    print("Connessione Command stabilita")
    # Accetta una connessione per l'heartbeat
    recive_heartbeat, address2 = socket_heartbeat.accept()
    print("Connessione Heartbeat stabilita")

    # Avvia il thread per gestire gli heartbeat
    thread_heartbeat = threading.Thread(
        target=hearthbeat_receive, args=(recive_heartbeat,)
    )
    thread_heartbeat.start()

    # Gestione dei comandi
    while not heartbeat_lost:
        try:
            message = recive_command.recv(BUFFER_SIZE)
            if not message:
                print("Connessione chiusa dal client per i comandi")
                break

            # Decodifica del messaggio ricevuto
            string = message.decode().split("|")
            if len(string) == 2:
                command = string[0]
                value = string[1]
                print(f"Comando ricevuto: {command} con valore {value}")

                # Esecuzione del comando se valido
                if command in commands:
                    if value == "start":  # Inizia a muoversi
                        commands[command]()  # Esegue la funzione associata al comando
                        response = f"ok|Comando {command} iniziato"
                    elif value == "stop":  # Ferma il movimento
                        alice.stop()
                        response = f"ok|Comando {command} fermato"
                    else:
                        response = "error|Valore non valido"
                else:
                    response = "error|Comando non riconosciuto"
            else:
                response = "error|Formato del messaggio non valido"

            # Invio della risposta al client
            recive_command.send(response.encode())
        except Exception as e:
            print(f"Errore durante la gestione dei comandi: {e}")
            break

    # Ferma il robot e chiude le connessioni se l'heartbeat è perso
    alice.stop()
    recive_command.close()
    recive_heartbeat.close()
    socket_command.close()
    socket_heartbeat.close()
    print("Connessioni chiuse e server terminato")

if __name__ == "__main__":
    main()
