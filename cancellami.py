def hearthbeat_recive(recive_heartbeat):
    socket_heartbeat.settimeout(6.5)
    while True:
        try:
            data = recive_heartbeat.recv(4092)
            print("up")
        except socket.timeout:
            print("FERMA TUTTO")
            break #Esci dal ciclo se c'è un timeout
        except Exception:
            print("si è verificato un errore : {e}")
            break#Esci dal ciclo in caso di errori non previsti

socket_heartbeat.close()
socket_command.close()
AlphaBot.stop

#Associa il socket a un indirizzo e una porta 
socket_command.bind(("localhost", 12345))
socket_heartbeat.bind(("localhost",12346))

#il server ascolta le connesioni in entrata 
socket_command.listen(1)
socket_heartbeat.listen(1)
print("Server TCP in attesa di connessioni....")

#accetta una connesione 
recive_command, address1 = socket_command.accept() #bloccante
print("Connesione Command")
recive_heartbeat, address2 = socket_heartbeat.accept() #Bloccante
print("Connessione Heartbeat")

thread_heartbeat = threading.Thread(target = heartbeat_recive, args=(recive_heartbeat,))
thread_heartbeat.start()
