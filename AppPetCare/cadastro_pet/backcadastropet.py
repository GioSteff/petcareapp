import sqlite3 as lite

con = lite.connect('cadastros_pet.db')

# CRUD - create, read, update, delete

# Insert data
def insert_form(i):
    with con:
        cur = con.cursor()
        query = ('''
            INSERT INTO cadastro (
                nome,
                genero,
                especie,
                idade,
                raca,
                imagem,
                microchip,
                data_nascimento,
                data_adocao,
                numero_contato,
                castrado,
            )
            
            VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
    ''')
        cur.execute(query, i)



# update data
def update_data(i):
    with con:
        cur = con.cursor()
        query = ('''
            UPDATE cadastro SET
                nome=?,
                genero=?,
                especie=?,
                idade=?,
                raca=?,
                imagem=?,
                microchip=?,
                data_nascimento=?,
                data_adocao=?,
                numero_contato=?,
                castrado=?,
            WHERE id=?
    ''')
        cur.execute(query, i)



# Delet data
def del_data(i):
    with con:
        cur = con.cursor()
        query = 'DELETE FROM cadastro WHERE id=?'
        cur.execute(query, i)



# View data
def view_data_fun():
    view_data = []
    with con:
        cur = con.cursor()
        query = 'SELECT * FROM cadastro'
        cur.execute(query)

        rows = cur.fetchall()
        for row in rows:
            view_data.append(row)
    return view_data



# View individual data
def view_item(id):
    view_individual_data = []
    with con:
        cur = con.cursor()
        query = 'SELECT * FROM cadastro WHERE id=?'
        cur.execute(query, id)

        rows = cur.fetchall()
        for row in rows:
            view_individual_data.append(row)
    