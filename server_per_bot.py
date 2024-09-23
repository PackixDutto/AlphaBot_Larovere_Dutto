import socket

MY_ADDRESS = ("192.168.1.119", 9090)
BUFFER_SIZE = 4096

commands = ["forward", "backward", "left", "right"]
#Client gira sul computer, processo server gira sul robot. Messaggi di due tipi: richieste (client a server) risposte (server a client)
#richieste: f"{command}|{value}"
#risposte: f"{status}|{phrase}" status = ok o error, phrase = frase dell'errore avvenuto
#comandi possibili: forward, backward, left, right
#Server TCP che gestisca un singolo client (più facile perché non usiamo i thread)
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Creo il socket
    server_socket.bind(MY_ADDRESS)  #Associo il socket all'indirizzo IP e alla porta
    server_socket.listen()  #Mi metto in ascolto, in attesa di connessioni

    print("Server in ascolto su", MY_ADDRESS)

    while True:
        client_socket, client_address = server_socket.accept()  #Accetto la connessione dal client
        print(f"Connessione stabilita con {client_address}")

        connection_open = True
        while connection_open:
            message = client_socket.recv(BUFFER_SIZE)  #Ricevo il messaggio
            if not message:
                #Se il messaggio è vuoto, il client ha chiuso la connessione
                print(f"Connessione chiusa da {client_address}")
                connection_open = False
                continue

            string = message.decode().split("|")
            if len(string) == 2:
                command = string[0]
                value = string[1]

                if command in commands:
                    status = "ok"
                    phrase = f"Comando {command} eseguito con valore {value}"
                    print(f"Ricevuto comando da {client_address}: {command} con valore {value}")
                else:
                    status = "error"
                    phrase = "Comando non esistente"
                    print(f"Errore: comando {command} non riconosciuto")
            else:
                status = "error"
                phrase = "Formato del messaggio non valido"
                print(f"Errore: messaggio malformato {message.decode()}")

            response = f"{status}|{phrase}"
            client_socket.send(response.encode())  #Invia la risposta al client

        client_socket.close()  #Chiudo il socket del client quando la connessione termina

    server_socket.close()  #Chiudo il socket del server quando termina il ciclo principale

if _name_ == "_main_":
    main()