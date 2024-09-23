import socket
#lista e fai elif x vane 
SERVER_ADDRESS = ("192.168.1.119", 9090)
BUFFER_SIZE = 4096

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    while True:
        command = input("inserisci che cosa vuoi che il robot faccia: forward per andare dritto, backward per andare indietro, left per andare a sinistra, right per andare a destra: ")
        value = input("inserisci un valore: ")
        message = f"{command}|{value}" #valore che mando al server
        s.sendall(message.encode()) #per trasmettere stringhe binarie
        stringa= s.recv(BUFFER_SIZE) #ritorna i dati e l'indirizzo
        x = stringa.decode().split("|")
        print(x)#stampa il messagio del server

        s.close()

if __name__ == "__main__":
    main()