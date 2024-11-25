import socket
import threading  # Per il controllo del heartbeat
import RPi.GPIO as GPIO
import time
import AlphaBot

# Indirizzo del server e dimensione del buffer
MY_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
alice = AlphaBot.AlphaBot()
alice.stop()

#Comandi del robot
commands = {"forward": alice.forward, "backward": alice.backward, "left": alice.left, "right": alice.right}

# Variabile di controllo condivisa per fermare il movimento del robot se il heartbeat fallisce
stop_robot_flag = threading.Event()

def heartbeat(client_socket):
    client_socket.settimeout(6.5)
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            print("Heartbeat ON.")
        except socket.timeout:
            print("FERMA TUTTO")
            alice.stop()  # Ferma il robot
            break
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            break

def main():
    #Creo il socket del server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(MY_ADDRESS)  # Associa al mio indirizzo
    server_socket.listen()  # Ascolta aspettando client

    print("Server in ascolto su", MY_ADDRESS)  # DEBUG

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione stabilita con {client_address}")

        #Avvio il thread per il controllo dell'heartbeat
        heartbeat_thread = threading.Thread(target=heartbeat, args=(client_socket,))
        heartbeat_thread.start()

        connection_open = True
        while connection_open and not stop_robot_flag.is_set():  # Controlla il flag
            try:
                message = client_socket.recv(BUFFER_SIZE)
                if not message:
                    print(f"Connessione chiusa da {client_address}")
                    connection_open = False
                    continue

                #Decodifico il messaggio ricevuto
                string = message.decode().split("|")
                if len(string) == 2:
                    command = string[0]
                    value = string[1]
                    print(f"Comando ricevuto: {command} con valore {value}")

                    if command == "c":
                        print(f"Connessione chiusa da {client_address}")
                        connection_open = False
                        continue

                    # Eseguo il comando
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
                client_socket.send(response.encode())
            except Exception as e:
                print(f"Errore durante la ricezione: {e}")
                break

        # Chiude il socket del client
        client_socket.close()

    #Chiude il socket del server
    server_socket.close()

if __name__ == "__main__":
    main()