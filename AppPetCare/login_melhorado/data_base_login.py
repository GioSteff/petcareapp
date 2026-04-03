import sqlite3 as lite

con = lite.connect('Usuarios_Cadastrados.db')

with con:
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Password TEXT NOT NULL,
                Confirm_Password TEXT NOT NULL,
                recovery_token TEXT,
                recovery_expiry TEXT
            );
        ''')