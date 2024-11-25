#CODICE WASD
import socket
import RPi.GPIO as GPIO
import time
import AlphaBot

# Indirizzo del server e dimensione del buffer
MY_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
alice = AlphaBot.AlphaBot()
alice.stop()

# Comandi disponibili per il robot
commands = {"forward": alice.backward, "backward": alice.forward, "left": alice.left, "right": alice.right}

def main():
    # Creazione del socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(MY_ADDRESS)
    server_socket.listen()

    print("Server in ascolto su", MY_ADDRESS)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione stabilita con {client_address}")

        connection_open = True
        while connection_open:
            message = client_socket.recv(BUFFER_SIZE)
            if not message:
                print(f"Connessione chiusa da {client_address}")
                connection_open = False
                continue

            #Decodifica del messaggio ricevuto
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

            #Invio della risposta al client
            client_socket.send(response.encode())

        client_socket.close()

    server_socket.close()

if __name__ == "__main__":
    main()
