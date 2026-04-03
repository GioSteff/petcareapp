from __future__ import annotations
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import sqlite3 as lite
import hashlib
import time
import random
import string


class BackEndLogin():
    def __init__(self):
        self.con = lite.connect('Usuarios_Cadastrados.db')

    def connect_db(self):
        self.cursor = self.con.cursor()

    def disconnect_db(self):
        self.con.close()

    def verify_recovery_columns(self):
         '''Verifica se ass colunas de recuperação existem e cria se necessário'''
         try:
             self.connect_db()

             # Verifica se a coluna recovery_token existe
             self.cursor.execute('PRAGMA table_info(Usuarios)')
             columns = [column[1] for column in self.cursor.fetchall()]

             if 'recovery_token' not in columns:
                  self.cursor.execute('ALTER TABLE Usuarios ADD COLUMN recovery_token TEXT')

             if 'recovery_expiry' not in columns:
                  self.cursor.execute('ALTER TABLE Usuarios ADD COLUMN recovery expiry TEXT')

             self.con.commit()
             self.disconnect_db()
             return True
         except Exception as e:
              messagebox.showerror('Erro', f'Erro ao verificar/criar colunas: {e}')
              return False

    def insert_info(self, username, email, password, confirm_password):
        
            self.cursor.execute('''
                INSERT INTO Usuarios (
                    Username,
                    Email,
                    Password,
                    Confirm_Password
                )
                          
                VALUES (
                    ?,
                    ?,
                    ?,
                    ?
                )
            ''', (username, email, password, confirm_password))
            self.con.commit()

    def update_info(self, user_id, username, email, password, confirm_password):
            self.cursor = self.con.cursor()
            self.cursor.execute('''
                UPDATE Usuarios SET
                          Username=?,
                          Email=?,
                          Password=?,
                          Confirm_Password=?
                        WHERE id=?
            ''', (username, email, password, confirm_password, user_id))
            self.con.commit()

    def delete_info(self, user_id):
            self.cursor = self.con.cursor()
            self.cursor.execute('DELETE FROM Usuarios WHERE id=?', (user_id,)) # Vírgula para ser tupla
            self.con.commit()

    # Métodos de recuperação de senha

    def verify_existing_email(self, email):
         self.connect_db()
         self.cursor.execute('SELECT * FROM Usuarios WHERE email=?', (email,))
         user = self.cursor.fetchone()
         self.disconnect_db()
         return user is not None
    
    def generate_recovery_token(self, email):
        timestamp = str(time.time() + 3600)  # 1 hora de validade
        token = hashlib.sha256(f"{email}{timestamp}".encode()).hexdigest()
        return token, timestamp
    
    def save_recovery_token(self, email, token, expiry):
         try:
              self.connect_db()
              self.cursor.execute('''
                       UPDATE Usuarios
                       SET recovery_token=?, recovery_expiry=?
                       WHERE email=?
                ''', (token, expiry, email))
              self.con.commit()
              self.disconnect_db()
              return True
         except Exception as e:
              messagebox.showerror('Erro', f'Erro ao salvar token:{e}')
              return False
         
    def validate_recovey_token(self, token):
         try:
              self.connect_db()
              current_time = time.time()

              self.cursor.execute('''
                    SELECT email FROM Usuarios
                    WHERE recovery_token=? AND CAST(recovery_expiry AS REAL) > ?''', (token, current_time))
              
              result = self.cursor.fetchone()
              self.disconnect_db()

              return result[0] if result else None
         except Exception as e:
              messagebox.showerror('Erro', f'Erro ao validar token: {e}')
              return None
         
    def update_password_with_token(self, email, new_password, token):
         try:
              self.connect_db()
              self.cursor.execute('''
                    UPDATE Usuario
                    SET Password=?, Confirm_Password=?, recovery_token=NULL, recovery_expiry=NULL
                    WHERE email=? AND recovery_token=?
                ''', (new_password, new_password, email, token))
              self.con.commit()
              afected_lines = self.cursor.rowcount
              self.disconnect_db()
              return afected_lines > 0
         except Exception as e:
              messagebox.showerror('Erro', f'Erro ao atualizar senha: {e}')
              return False
         
    def generate_temp_password(self):
         return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
         

    # Aparentemente devem estar só no frontend
    # def clean_entry_register(self):
    #     self.username_register_entry.delete(0, END)
    #     self.email_register_entry.delete(0, END)
    #     self.password_register_entry.delete(0, END)
    #     self.password_confirm_entry_register.delete(0, END)

    # def clean_entry_login(self):
    #     self.username_login_entry.delete(0, END)
    #     self.password_login_entry.delete(0, END)

    def register_user(self, username, email, password, confirm_password):
        try: 
            if not all([username, email, password, confirm_password]):
                messagebox.showerror('Erro', 'Preencha todos os campos.')
                return

            elif (len(username)) < 3:
                messagebox.showwarning('Aviso', 'Username deve conter pelo menos 3 caracteres.')
                return
            
            elif (len(password)) < 6:
                messagebox.showwarning('Aviso', 'Sua senha deve conter pelo menos 6 caracteres.')
                return
            
            elif confirm_password != password:
                messagebox.showwarning('Aviso', 'A confirmação da senha deve condizer com a senha.')  
                return    

            elif not email.endswith('@gmail.com'):
                messagebox.showerror('Erro', 'Caminho de e-mail inválido.')  
                return
            
            elif email == '@gmailcom':
                messagebox.showerror('Erro', 'E-mail inválido.')
                return
            
            else:
                self.connect_db()
                # Verifica se email já existe:
                self.cursor.execute('SELECT * FROM Usuarios WHERE email=?', (email,))
                if self.cursor.fetchone():
                     messagebox.showerror('Erro', 'Este email já está cadastrado')
                     self.disconnect_db()
                     return False
                
                self.insert_info(username, email, password, confirm_password)
                #self.clean_entry_register()
                self.disconnect_db()
                messagebox.showinfo('Confirmação', f'Cadastro realizado com sucesso.\nSeja bem-vindo {self.username_register}')

        except Exception as e:
            self.con.rollback()
            messagebox.showerror('Erro', f'Erro ao efetivar o cadastro:\n{e}.\nPor favor, tente novamente!')
            return False

    def verify_login(self, username, password):

        if not username or not password:
            messagebox.showwarning('Aviso', 'Preencha os campos corretamente.')
            return
        
        try:
            self.connect_db()

            self.cursor.execute(
                'SELECT * FROM Usuarios WHERE Username=? AND Password=?', (username,password)
            )
            verify_data = self.cursor.fetchone()
            self.disconnect_db() # Percorre a tela de usuários

            if verify_data: 
                messagebox.showinfo(f'Aviso', f'Bem-vindo ao sistema PetCare {username}!')
                #self.clean_entry_login()
                self.disconnect_db()
            else:
                messagebox.showerror('Erro', 'Falha ao efetuar o login,\ndados não encontrados.\nCaso não possua uma conta,\ncadastre-se antes.')
                self.disconnect_db()
        except Exception as e:
            if hasattr(self, 'con'):
                self.disconnect_db()
                messagebox.showerror('Erro', f'Erro ao conectar ao banco de dados: {str(e)}')


