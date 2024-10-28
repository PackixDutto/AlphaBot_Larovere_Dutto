import sqlite3

# Connessione al database (crea il file se non esiste)
conn = sqlite3.connect('mio_database.db')
cur = conn.cursor()

# Creazione della tabella (se non esiste)
# La tabella ha una colonna 'tasto' (PRIMARY KEY) e una 'azione' associata al tasto
cur.execute('''
    CREATE TABLE IF NOT EXISTS comandi (
        tasto VARCHAR(1) PRIMARY KEY,
        azione TEXT
    )
''')

comandi = [
    ('u', 'F100'),  # Avanza di 100
    ('i', 'L40'),   # Gira a sinistra di 40
]


cur.executemany('INSERT OR REPLACE INTO comandi (tasto, azione) VALUES (?, ?)', comandi)
conn.commit()

print("Tabella comandi creata e popolata con successo.")
conn.close()


######bisogna passare questo in client_per_robot in qualche modo 