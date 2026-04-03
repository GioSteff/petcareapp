from __future__ import annotations
import backendlogin
import google_auth
from google_auth import GoogleAuth
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from tkinter import Tk, StringVar, ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
import sqlite3 as lite
from tkinter import Toplevel
import tkinter as tk
from io import BytesIO
import re
import threading
import string
import random
import yagmail
import random
import string
import hashlib
import time
from yagmail import *



# Cores
w = 'white'
p = 'pink'
b = 'black'
fundo = '#242424'
entradas = '#343638'
escrita = '#9E9E9E'

class App(ctk.CTk, backendlogin.BackEndLogin):
    def __init__(self):
        ctk.CTk.__init__(self)
        backendlogin.BackEndLogin.__init__(self)
        self.initial_window_config()
        self.google_auth = GoogleAuth()
        self.login_screen()
        self.current_token = None
        self.current_email = None

    # Configurações da janela inicial 
    def initial_window_config(self):
        self.geometry('412x917')
        self.title('OhMyPet!')
        self.resizable(False,False)

    def login_screen(self):

        if hasattr(self, 'frame_register'):
          self.frame_register.place_forget()

        if hasattr(self, 'frame_recover'):
            self.frame_recover.place_forget()

        # Imagens
        self.img = ctk.CTkImage(
            light_image=Image.open('cat4.png'), # tema escuro e tema claro
            dark_image=Image.open('cat4.png'),
            size=(300,200)
        )
        self.lb_img = ctk.CTkLabel(
            self,
            text=None,
            image=self.img
        )
        self.lb_img.place(relx=0.5, rely=0.21, anchor='center') # centralizar

        self.update_main_title('Faça seu login ou \ncadastre-se na PetCare')

        # # Título da plataforma
        # self.title_label = ctk.CTkLabel(
        #     self,
        #     text='Faça seu login ou \ncadastre-se na PetCare',
        #     font=('Century Gothic', 14, 'bold')
        # )
        # self.title_label.place(relx=0.5, rely=0.03, anchor='center')

        # Frame de formulário de login
        self.frame_login = ctk.CTkFrame(
            self,
            width=220,
            height=800
        )
        self.frame_login.place(x=45, y=290)

        # Widgets 
        self.lb_title = ctk.CTkLabel(
            self.frame_login,
            text='🐾Faça o seu login!',
            font=('Century Gothic', 22, 'bold'),
            text_color=w
        )
        self.lb_title.grid(row=0, column=0, padx=10, pady=15)

        self.username_login_entry = ctk.CTkEntry(
            self.frame_login,
            width=300,
            height=60,
            placeholder_text='Nome de usuário...',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color=p
        )
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=15)

        self.password_login_entry = ctk.CTkEntry(
            self.frame_login,
            width=300, 
            height=60,
            placeholder_text='Senha...',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color=p,
            show='*'
        )
        self.password_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.check_password = ctk.CTkCheckBox(
            self.frame_login,
            text='Ver senha',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            border_color=p,
            command=self.toggle_password
        )
        self.check_password.grid(row=3, column=0, padx=10, pady=0)

        self.forgot_password_button = ctk.CTkButton(
            self.frame_login,
            width=300,
            height=20,
            text='Esqueceu a senha',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=w,
            command=self.recover_password_screen
        )
        self.forgot_password_button.grid(row=4, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(
            self.frame_login,
            width=300,
            text='Login',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=w,
            command=self.verify_login
        )
        self.btn_login.grid(row=5, column=0, padx=10, pady=20)

        
        self.google_button = ctk.CTkButton(
            self.frame_login,
            width=150,
            height=20,
            text='Entrar com google',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=w,
            command=self.google_login
        )
        self.google_button.grid(row=6, column=0, padx=10, pady=0)

        self.span = ctk.CTkLabel(
            self.frame_login,
            text='Não possui conta?\nCadastre-se clicando no botão abaixo:',
            font=('Century Gothic', 12, 'bold')
        )
        self.span.grid(row=7, column=0, padx=10, pady=(100, 10))

        self.register_button = ctk.CTkButton(
            self.frame_login,
            text='Cadastre-se',
            font=('Century Gothic', 14, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=w,
            command=self.register_screen
        )
        self.register_button.grid(row=8, column=0, padx=10, pady=10)

    def recover_password_screen(self):
        '''Tela de recuperação de senha'''

        self.frame_login.place_forget()
        self.update_main_title('Recuperação de senha')

        self.frame_recover = ctk.CTkFrame(
            self,
            width=220,
            height=800
        )
        self.frame_recover.place(relx=0.5, rely=0.5, anchor='center')

        self.recover_title = ctk.CTkLabel(
            self.frame_recover,
            text='Recuperar senha',
            font=('Century Gothic', 22, 'bold'),
            text_color=w
        )
        self.recover_title.grid(row=0, column=0, padx=20, pady=10)

        # Instrução
        self.recover_instruction = ctk.CTkLabel(
            self.frame_recover,
            text='Digite seu e-mail cadastrado:\nEnviaremos instruções para redefinir sua senha.',
            font=('Century Gothic', 12, 'bold'),
            justify='center'
        )
        self.recover_instruction.grid(row=1, column=0, padx=20, pady=10)

        # Campo de email
        self.recover_email_entry = ctk.CTkEntry(
            self.frame_recover,
            width=300,
            height=60,
            placeholder_text='Seu e-mail...',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color=p
        )
        self.recover_email_entry.grid(row=2, column=0, padx=10, pady=10)

        # Botão enviar
        self.recover_send_button = ctk.CTkButton(
            self.frame_recover,
            width=300,
            text='Enviar',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=w,
            command=self.send_recovery_email
        )
        self.recover_send_button.grid(row=3, column=0, padx=10, pady=15)

        # Botão voltar
        self.recover_back_button = ctk.CTkButton(
            self.frame_recover,
            text='Voltar ao login',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            fg_color=w,
            hover_color=p,
            text_color=b,
            border_width=2,
            border_color=w,
            command=self.login_screen
        )
        self.recover_back_button.grid(row=4, column=0, padx=10, pady=5)


    # def send_recovery_email(self):
    #     email = self.recover_email_entry.get()

    #     if not email:
    #         messagebox.showwarning('Aviso', 'Informe seu e-mail')
    #         return
        
    #     if self.verify_existing_email(email):
    #         # Gera token único
    #         token, expiry = self.generate_recovery_token(email)
    #         self.save_recovery_token(email, token, expiry)

    #         # Enviando email
    #         try:
    #             # Credenciais do email criado para o programa
    #             yag.send(
    #                 to=email,
    #                 subject='Recuperação de senha - OhMyPet!',
    #                 contents=f'''Olá!
    #                 Você solicitou recuperaçção de senha no OhMyPet!
                    
    #                 📌 CÓDIGO DE VERIFICAÇÃO: {token}

    #                 Instruções:
    #                 1. Abra o aplicativo
    #                 2. Digite este código
    #                 3. Crie sua nova senha

    #                 Código válido por 1 hora.

    #                 Equipe OhMyPet'''
    #             )

    #             messagebox.showinfo('Sucesso', 'E-mail enviado! Verifique sua caixa de entrada.')

    #             # Tela para digitar código
    #             self.enter_recovery_code_screen(email)

    #         except Exception as e:
    #             messagebox.showerror('Erro', f'Falha ao enviar email: {str[e]}')

    #     else:
    #         messagebox.showerror('Erro', 'E-mail não encontrado no sistema.')


    def enter_recovery_code_screen(self, email):
        '''Tela para usuário inserir o código token'''

        if hasattr(self, 'frame_recover'):
            self.frame_recover.place_forget()

        self.frame_code = ctk.CTkFrame(
            self,
            width=220,
            height=800
        )
        self.frame_code.place(relx=0.5, rely=0.5, anchor='center')

        ctk.CTkLabel(
            self.frame_code,
            text='Insira o código token...',
            font=('Century Gothic', 22, 'bold'),
            text_color=w
        ).grid(row=0, column=0, padx=20, pady=10)

        # Email (informativo)
        ctk.CTkLabel(
            self.frame_code,
            text=f'Enviado para:\n{email}',
            font=('Century Gothic', 12),
            justify='center'
        ).grid(row=1, column=0, padx=20, pady=10)

        # Campo do código
        self.code_entry = ctk.CTkEntry(
            self.frame_code,
            width=300,
            height=60,
            placeholder_text='Digite o código...',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color=p
        )
        self.code_entry.grid(row=2, column=0, padx=10, pady=10)

        # Botão verificar
        ctk.CTkButton(
            self.frame_code,
            width=300,
            text='Verificar código',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            command=lambda: self.verify_code(email) # fazer função
        ).grid(row=3, column=0, padx=10, pady=15)

        # Botão reenviar
        ctk.CTkButton(
            self.frame_code,
            width=300,
            text='Reenviar código',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            command=lambda: self.resend_code(email) # fazer função
        ).grid(row=4, column=0, padx=10, pady=5)

    def verify_code(self, email):

        code = self.code_entry.get()

        if not code:
            messagebox.showwarning('Aviso', 'Digite o código de recuperação de e-mail.')
            return
        
        email_valido = self.validate_recovey_token(code)

        if email_valido and email_valido == email:
            self.current_token = code
            self.current_email = email

            if hasattr(self, 'frame_code'):
                self.frame_code.place_forget()

            self.new_password_screen()
        
        else:
            messagebox.showerror('Erro', 'Código inválido ou expirado.')

    # def new_password_screen(self):



            

    
                
            
    # def send_recovery_email(self):
    #     '''Envia email de recuperação'''

    #     temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    #     email = self.recover_email_entry.get()

    #     if not email:
    #         messagebox.showwarning('Aviso', 'Informe seu e-mail')
    #         return
        
    #     # Verifica se email existe no banco
    #     try:
    #         self.connect_db()
    #         self.cursor.execute('SELECT * FROM Usuarios WHERE email=?', (email,))
    #         user = self.cursor.fetchone()
    #         self.disconnect_db()

    #         if user:
    #            # Configuração do email
    #            yag = yagmail.SMTP('seuemail@gmail.com', 'sua senha')

    #            yag.send(
    #               to=email,
    #               subject='Recuperação de senha - OhMyPet!',
    #               contents=f'Sua nova senha temporária é: {temp_password}\nFaça login e altere sua senha.'
    #             )
               
    #            self.update_password_in_db(email, temp_password)

    #            messagebox.showinfo('Sucesso', 'E-mail de recuperação enviado.')
    #            # Volta para tela de login
    #            self.login_screen()
    #         else:
    #             messagebox.showerror('Erro', 'E-mail não encontrado no sistema')
    #     except Exception as e:
    #         messagebox.showerror('Erro', f'Erro ao verificar o e-mail: {str(e)}')

    def update_password_in_db(self, email, temp_password):
        try:
            self.connect_db()
            self.cursor.execute('UPDATE Usuarios SET senha=? WHERE email=?', (temp_password, email))
            self.con.commit() # salvar
            self.disconnect_db()
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao atualizar senha: {e}')


    def update_main_title(self, text):
        if hasattr(self, 'title_label'):
            if self.title_label.winfo_exists():
                self.title_label.configure(text=text)
            else:
                self.title_label = ctk.CTkLabel(
                    self,
                    text=text,
                    font=('Century Gothic', 20, 'bold'),
                    justify='center'
                )
                self.title_label.place(relx=0.5, rely=0.08, anchor='center')
        else:
            self.title_label = ctk.CTkLabel(
                self,
                text=text,
                font=('Century Gothic', 20, 'bold'),
                justify='center'
            )
            self.title_label.place(relx=0.5, rely=0.08, anchor='center')

    def google_login(self):
        '''Método para login com google'''
        try:
            # Mostrar loading
            self.show_loading('Abrindo navegador de autentificação...')

            # Executar em thread separada para não travar a interface
            def auth_thread():
                try:
                    self.google_auth.authenticate(self.google_login_callback)
                except Exception as e:
                    self.after(0, lambda: messagebox.showerror('Erro', f'Falha na autentificação: {str(e)}'))
                finally:
                    self.after(0, self.hide_loading)
            
            threading.Thread(target=auth_thread, daemon=True).start()
        
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao iniciar login Google: {str(e)}')

    def google_login_callback(self, user_data):
        '''Calback após o sucesso na autentificação'''

        # Tudo que envolve banco de dados deve voltar para thread principal
        self.after(0, lambda: self._process_google_login(user_data))

    def _process_google_login(self, user_data):
        # Verificar se ouve erro
        if isinstance(user_data, dict) and 'error' in user_data:
            messagebox.showerror('Erro', f"Falha na autentificação: {user_data['error']}")
            return
        
        # Verificar se os dados existem
        try:
            email = user_data['email']
            name = user_data.get('name', 'Usuário')
            username = name.replace(' ', '_').lower()

            # Conectar ao banco
            self.connect_db()
            self.cursor.execute('SELECT * FROM Usuarios WHERE Email=?', (email,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                # Login automático
                messagebox.showinfo('Sucesso', f'Bem-vindo(a) de volta, {name}!')
                # Abrir a tela inicial futuramente
            else:
                # Criar novo usuário
                temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

                # Inserir no banco
                self.insert_info(username, email, temp_password, temp_password)
                messagebox.showinfo('Cadastro', f'Conta criada com sucesso, {name}!')

            self.disconnect_db()

        except KeyError as e:
            messagebox.showerror('Erro', f'Dados incompletos recebidos: {str(e)}')
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao processar: {str(e)}')

    def show_loading(self, message):
        '''Mostrar indicador de loading'''
        self.loading_frame = ctk.CTkFrame(
            self,
            width=300,
            height=100
        )
        self.loading_frame.place(relx=0.5, anchor='center')

        self.loading_label = ctk.CTkLabel(
            self.loading_frame,
            text=message,
            font=('Century Gothic', 14)
        )
        self.loading_label.pack(pady=20)

        self.progressbar = ctk.CTkProgressBar(self.loading_frame)
        self.progressbar.pack(pady=10)
        self.progressbar.start()

    def hide_loading(self):
        '''Esconde indicador de loading'''
        if hasattr(self, 'loading_frame'):
            self.loading_frame.place_forget()

    def register_screen(self): # Fazer mudar o texto de cima e a imagem
        # Remover o formulário de login
        self.frame_login.place_forget()

        # Frame do formulário de login
        self.update_main_title('Realize o cadastro para começar\nsua jornada na PetCare!')
        self.frame_register = ctk.CTkFrame(
            self,
            width=220,
            height=800
        )
        self.frame_register.place(x=45, y=290)

        self.lb_title = ctk.CTkLabel(
            self.frame_register,
            text='🐾Faça o seu cadastro!',
            font=('Century Gothic', 22, 'bold'),
            text_color='white'
            )
        self.lb_title.grid(row=0, column=0, padx=10, pady=15)

        # Widgets da tela de cadastro
        self.username_register_entry = ctk.CTkEntry(
            self.frame_register,
            width=300,
            height=60,
            placeholder_text='Nome de usuário..',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color='pink'
            )
        self.username_register_entry.grid(row=1, column=0, padx=10, pady=15)

        self.email_register_entry = ctk.CTkEntry(
            self.frame_register,
            width=300,
            height=60,
            placeholder_text='E-mail..',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color='pink'
            )
        self.email_register_entry.grid(row=2, column=0, padx=10, pady=15)

        self.password_register_entry = ctk.CTkEntry(
            self.frame_register,
            width=300,
            height=60,
            placeholder_text='Senha..',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color='pink',
            show='*'
            )
        self.password_register_entry.grid(row=3, column=0, padx=10, pady=15)

        self.password_confirm_entry_register = ctk.CTkEntry(
            self.frame_register,
            width=300,
            height=60,
            placeholder_text='Confirme a senha..',
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            border_color='pink',
            show='*'
            )
        self.password_confirm_entry_register.grid(row=4, column=0, padx=10, pady=15)

        self.check_register_password = ctk.CTkCheckBox(
            self.frame_register,
            text='Ver senha',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            border_color=p,
            command=self.toggle_register_password
        )
        self.check_register_password.grid(row=5, column=0, padx=10, pady=15)

        self.btn_register = ctk.CTkButton(
            self.frame_register,
            width=300,
            text='Cadastrar',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color='pink', # cor do botão
            hover_color='white', # cor do botão quando passa o mouse em cima 
            text_color='black',
            border_width=2,
            border_color='white',
            command=self.register_user # talvez tenha que tirar
        )
        self.btn_register.grid(row=6, column=0, padx=10, pady=10)

        self.btn_back_login = ctk.CTkButton(
            self.frame_register,
            text='Fazer login',
            font=('Century Gothic', 14, 'bold'),
            corner_radius=20,
            fg_color='white', # cor do botão
            hover_color='pink', # cor do botão quando passa o mouse em cima 
            text_color='black',
            border_width=2,
            border_color='pink',
            command=self.login_screen
            )
        self.btn_back_login.grid(row=7, column=0, padx=10, pady=5)

    def clean_entry_register(self): # apaga informações inseridas
        self.username_register_entry.delete(0, END)
        self.email_register_entry.delete(0, END)
        self.password_register_entry.delete(0, END)
        self.password_confirm_entry_register.delete(0, END)

    def clean_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)

    def toggle_password(self):
        if self.check_password.get():
            self.password_login_entry.configure(show='')
        else:
            self.password_login_entry.configure(show='*')

    def toggle_register_password(self):
        if self.check_register_password.get():
            self.password_register_entry.configure(show='')
        else:
            self.password_register_entry.configure(show='*')

if __name__== '__main__':
    app = App()
    app.mainloop()

# Corrigir erros
# Fazer tema claro e escuro
# Incluir logar com google (cadastrar tmb talvez)
# Incluir esqueci minha senha
# Ao invés de usar destroy usar forget
# Fazer tela de introdução antes do login 
# Depois do login levar pra tela inicial
# Arrumar tela de cadastro

# Incluir botão de recuperação de senha
# Incluir botão para manter logado
# Incluir botão pra sair da conta

# def send_recovery_email_real(self, email, temp_password):
#     yag = yagmail.SMTP('seuemail@gmail.com', 'sua senha')
#     yag.send(
#         to=email,
#         subject='Recuperação de senha - OhMyPet!',
#         contents=f'Sua nova senha temporária é: {temp_password}\nFaça login e altere sua senha.'
#     )