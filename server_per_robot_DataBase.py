#CODICE WASD
import socket
import RPi.GPIO as GPIO
import AlphaBot
import sqlite3

#Indirizzo del server e dimensione del buffer
MY_ADDRESS = ("192.168.1.123", 9999)
BUFFER_SIZE = 4096
alice = AlphaBot.AlphaBot()
alice.stop()

# Comandi disponibili per il robot
commands = {"forward": alice.forward, "backward": alice.backward, "left": alice.left, "right": alice.right}

def main():
    # Creazione del socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(MY_ADDRESS)
    server_socket.listen()

    print("Server in ascolto su", MY_ADDRESS)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connessione stabilita con {client_address}")

        #Mi connetto al database
        conn = sqlite3.connect('mio_databaseLarovere.db')
        cur = conn.cursor() #Faccio girare il database
        query = '''SELECT * 
            FROM comandi'''
        print(query)
        cur.execute(query) #Esegue la query SQL, recuperando tutti i risultati dalla tabella comandi
        conn.commit()
        connection_open = cur.fetchall()
        print(connection_open) #DEBUG

        while True:
            message = client_socket.recv(BUFFER_SIZE)

            if connection_open:
                query = f'''SELECT str_mov
                FROM comandi
                WHERE comandi.P_K = "{message}"'''

                cur.execute(query)
                rispo = cur.fetchall()
                risp = rispo[0]
                comando = risp[0]
                print(comando) #DEBUG

                list_comandi = comando.split(",")
                print(list_comandi) #DEBUG

                for c in list_comandi:
                    print(c[0]) #DEBUG LETTERA
                    if c[0] in commands:
                        print(c[1:]) #debug movimento
                    else:
                        print("Errore! Il tasto del comando selezionato non esiste")

        #client_socket.close()
    #server_socket.close()
if __name__ == "__main__":
    main()
