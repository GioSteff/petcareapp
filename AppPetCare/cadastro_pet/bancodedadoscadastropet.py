import sqlite3 as lite

# criando conexão
con = lite.connect('cadastros_pet.db')

# criando tabela
with con:
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE cadastro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            genero TEXT, 
            especie TEXT,
            idade INTEGER,
            raca TEXT,
            imagem BLOB,
            microchip TEXT,
            data_nascimento DATE,
            data_adocao DATE,
            numero_contato TEXT,
            castrado TEXT,
            
            
                
        )
    ''')

#       File "c:\python\AppPetCare\cadastro_pet\bancodedadoscadastropet.py", line 9, in <module>
#     cur.execute('''
#     ~~~~~~~~~~~^^^^
#         CREATE TABLE cadastro (
#         ^^^^^^^^^^^^^^^^^^^^^^^
#     ...<10 lines>...
#         )
#         ^
#     ''')
#     ^^^^
# sqlite3.OperationalError: table cadastro already exists
# PS C:\python\AppPetCare> 
