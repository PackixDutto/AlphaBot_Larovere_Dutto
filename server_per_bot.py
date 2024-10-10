import socket
import RPi.GPIO as GPIO
import time
import AlphaBot

from pynput import keyboard #X controllo robot movimento da tastiera

#funzione chiamata quando un tasto viene premuto 
def on_press(key):
    #try
    if key.char == "w":
        print("press w")
# expect AttributeError:
# ignora tasti speciali come Shift, Crel, etc
#pass
#funzione chiamata quando un tasto viene rilasciato 
def on_release(key):
    #try:
    if key.char == "w":
        print("release w")
#except AttributeError:
#       pass
def start_listener():
    #Listener per intercettare gli eventi da tastiera 
    with keyboard.listener(on_press = on_press, on_release = on_release) as listener:
            listener.join()

start_listener()

MY_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
alice = AlphaBot.AlphaBot()
alice.stop()

commands = ["forward", "backward", "left", "right"]

def main():
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

            string = message.decode().split("|")
            if len(string) == 2:
                command = string[0]
                value = string[1]
                print(command)
                print(value)

                if command in commands:
                    status = "ok"
                    phrase = f"Comando {command} eseguito con valore {value}"
                    print(f"Ricevuto comando da {client_address}: {command} con valore {value}")
                    if command == commands[0]:
                        alice.forward()
                    elif command == commands[1]:
                        alice.backward()
                    elif command == commands[2]:
                        alice.left()
                    elif command == commands[3]:
                        alice.right()
                    time.sleep(float(value))  #Conversione del valore
                    alice.stop()
                else:
                    status = "error"
                    phrase = "Comando non esistente"
                    print(f"Errore: comando {command} non riconosciuto")
            else:
                status = "error"
                phrase = "Formato del messaggio non valido"
                print(f"Errore: messaggio malformato {message.decode()}")

            response = f"{status}|{phrase}"
            client_socket.send(response.encode())

        client_socket.close()

    server_socket.close()

if _name_ == "_main_":
    main()