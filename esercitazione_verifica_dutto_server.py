import socket
import threading
import sqlite3

def init_db():
    #se il file non esiste, verra creato nela directory corrente.
    conn = sqlite3.connect('file.db')
    
    #crea un cursore per eseguire comandi SQL nel contesto della connessione al database.
    cursor = conn.cursor()
    
    #tabella che memorizza le informazioni sui file condivisi, con i campi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id_file INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            tot_frammenti INTEGER NOT NULL
        )
    ''')
    

    #questa tabella memorizza i frammenti dei file, con i campi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frammenti (
            id_frammento INTEGER PRIMARY KEY,
            id_file INTEGER,
            n_frammento INTEGER,
            host TEXT,
            FOREIGN KEY (id_file) REFERENCES files (id_file)
        )
    ''')
    
    conn.commit()
    conn.close()


def handle_client(conn, addr):
    print(f"Connessione da {addr}")
    with conn:
        while True:
            data = conn.recv(1024).decode()
            #se vuoto chiude
            if not data:
                break
            
            #Chiama la funzione process_request per elaborare la richiesta ricevuta e generare una risposta.
            response = process_request(data)#data contiene la richiesta inviata dal client.

            #invia la risposta
            conn.sendall(response.encode())

def process_request(request):
    # Stabilisce una connessione al database SQLite denominato 'file.db'.
    conn = sqlite3.connect('file.db')
    
    # Crea un cursore per eseguire comandi SQL nel contesto della connessione al database.
    cursor = conn.cursor()
    
    try:
        #Presence = client vuole verificare un file con noe determinato
        if request.startswith("PRESENCE:"):
            #trova nome del file prendendo la parte successiva al prefisso ( grazie a :).
            nome_file = request.split(":")[1]
            
            #verificare se il file con nome nome_file esiste nella tabella 'files'.
            #la funzione exist restituisce 1 se il file e presente, 0 altrimenti.
            cursor.execute("SELECT EXISTS(SELECT 1 FROM files WHERE nome=?)", (nome_file,))
            
            #restituisce una tupla contenente un singolo elemento, (0 o 1) e `found` diventa True se il file esiste, altrimenti False.
            found = cursor.fetchone()[0] == 1
            
            # Restituisce la risposta al client in formato stringa;   indicando la presenza o meno del file.
            return f"FOUND:{found}"
        

            # Numero frammenti!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                # se ce scritto FRAG_COUNT = il client vuole conoscere il numero totale di frammenti per un file specifico.
        elif request.startswith("FRAG_COUNT:"):
            #trova nome del file prendendo la parte successiva al prefisso ( grazie a :).
            nome_file = request.split(":")[1]
            
            #esegue una query SQL per ottenere il numero totale di frammenti del file
            #con nome 'nome_file' dalla tabella 'files'.
            cursor.execute("SELECT tot_frammenti FROM files WHERE nome=?", (nome_file,))
            
            #ottiene il risultato della query. Se il file esiste, `result` conterra una tupla
            #con un singolo elemento (tot_frammenti). Se non esiste, `result` sara `None`.
            result = cursor.fetchone()
            
            #restituisce la risposta al client nel formato "FRAG_COUNT_RESP:<numero_frammenti>" se il file e presente.
            #altrimenti, restituisce "FRAG_COUNT_RESP:0" per indicare che il file non e presente o ha 0 frammenti.
            return f"FRAG_COUNT_RESP:{result[0]}" if result else "FRAG_COUNT_RESP:0"


        #ip dell'host er framento specifico!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


                #verifica se la richiesta inizia con il prefisso "HOST_FOR_FRAG:" = il client vuole conoscere l'host che ospita un frammento specifico di un file.
        elif request.startswith("HOST_FOR_FRAG:"):
            # Estrae il nome del file e il numero del frammento dalla richiesta.
            # Il nome del file e dopo il primo ":", mentre il numero del frammento e dopo il secondo ":".
            nome_file, n_frammento = request.split(":")[1], int(request.split(":")[2])
            
            #per ottenere l'id del file con nome 'nome_file' dalla tabella 'files'.
            #necessario per trovare il frammento specifico nella tabella 'frammenti'.
            cursor.execute("SELECT id_file FROM files WHERE nome=?", (nome_file,))
            id_file = cursor.fetchone()
            
            #se il file e stato trovato (id_file non e None), va avanti.
            if id_file:
                #esegue una query per ottenere l'host del frammento specificato (n_frammento) wper il file con id `id_file[0]` nella tabella 'frammenti'.
                cursor.execute(
                    "SELECT host FROM frammenti WHERE id_file=? AND n_frammento=?",
                    (id_file[0], n_frammento)
                )
                
                #se il frammento esiste, result conterra una tupla con un singolo elemento (host). Se non esiste, `result` sara `None`.
                result = cursor.fetchone()
                
                #restituisce la risposta al client nel formato "HOST_FOR_FRAG_RESP:<host>"
                #se l'host e stato trovato. Altrimenti, restituisce "HOST_FOR_FRAG_RESP:None".
                return f"HOST_FOR_FRAG_RESP:{result[0]}" if result else "HOST_FOR_FRAG_RESP:None"


        #IP di tutti gli host per i frammenti di un file!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    finally:
        conn.close()
    return "ERROR:Invalid Request"

def start_server():
    #per controllare che ci siano le tabelle
    init_db()
    
    #crea un socket TCP 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    
    # mette in modalita ascolto
    server.listen()
    print("Server in ascolto sulla porta 9999")
    
    # Ciclo infinito per accettare connessioni dai client.
    while True:
        #accetta una nuova connessione conn rappresenta l'oggetto connessione,
        #mentre addr contiene l'indirizzo del client connesso.
        conn, addr = server.accept()
        
        #crea un nuovo thread per gestire il client connesso. Chiama la funzione
        #handle_client passando l'oggetto connessione e l'indirizzo del client come argomenti.
        #questo consente al server di gestire pii client contemporaneamente.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        
        thread.start()

if __name__ == "__main__":
    start_server()

