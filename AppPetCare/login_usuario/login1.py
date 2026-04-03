# fazer opção pra poder entrar com o google
# fazer com que a tela de cadastro e a tela de login tenham textos diferentes em cima da imagem
# arrumar erro de login, mesmo quando efetua certo da erro, quando da erro n da pra efetuar depois
# fazer com que n de para botar o mesmo user de outros usuários

from __future__ import annotations
import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
import sqlite3

class BackEnd():
    def connect_db(self):
        self.conn = sqlite3.connect('Cadastros_Usuarios.db')
        self.cursor = self.conn.cursor()

    def desconnect_db(self):
        self.conn.close()

    def create_table(self):
        self.connect_db()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Password TEXT NOT NULL,
                Confirm_Password TEXT NOT NULL
            );
        ''')
        self.conn.commit()
        self.desconnect_db()

    def clean_entry_register(self):
        self.username_register_entry.delete(0, END)
        self.email_register_entry.delete(0, END)
        self.password_register_entry.delete(0, END)
        self.password_confirm_entry_register.delete(0, END)

    def clean_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.password_login_entry.delete(0, END)


    def register_user(self):
        self.username_register = self.username_register_entry.get()
        self.email_register = self.email_register_entry.get()
        self.password_register = self.password_register_entry.get()
        self.confirm_password_register = self.password_confirm_entry_register.get()
        
        try:
                    
            if (self.username_register == '' or self.email_register == '' or self.password_register == '' or self.confirm_password_register == ''):
                messagebox.showerror(title='Erro', message='Por favor, complete todos os campos.')
                return
                
            elif any(char.isdigit() for char in self.username_register):
                messagebox.showerror(title='Erro', message='O nome deve conter apenas letras.')
                return
                
            elif (len(self.username_register) < 4):
                messagebox.showwarning(title='Aviso', message='O nome de usuário deve possuir pelo menos 4 letras.')
                return
            
            elif (len(self.password_register) < 4):
                messagebox.showwarning(title='Aviso', message='A senha deve conter pelo menos 4 caracteres.')
                return
                
            elif self.confirm_password_register != self.password_register:
                messagebox.showerror(title='Erro', message='A confirmação de senha não corresponde com a senha informada.')
                return

            elif not self.email_register.endswith('@gmail.com'): # depois mudar pra aceitar outras entradas
                messagebox.showerror(title='Erro', message='Endereço de e-mail inválido.')
                return

            elif self.email_register == '@gmail.com':
                messagebox.showerror(title='Erro', message='E-mail inválido')
                return
        
            else:
                self.connect_db()

                self.cursor.execute('''
                INSERT INTO Usuarios (Username, Email, Password, Confirm_Password)
                VALUES (?, ?, ?, ?)''', (self.username_register, self.email_register, self.password_register, self.confirm_password_register))
                self.clean_entry_register()
                self.conn.commit()
                self.desconnect_db()
                messagebox.showinfo(title='Confirmação', message= f'Cadastro realizado com sucesso.\nSeja bem-vindo {self.username_register}')
                
        except:
            self.conn.rollback()
            messagebox.showerror(title='Erro', message='Erro ao efetivar o cadastro.\nPor favor, tente novamente!')
            #self.desconnect_db()
    
    def verify_login(self):
        username = self.username_login_entry.get()
        password = self.password_login_entry.get()

        if username == '' or password == '':
            messagebox.showerror(title='Erro', message='Por favor, preencha os campos corretamente.')
            return

        try:
            self.connect_db()

            self.cursor.execute('''SELECT * FROM Usuarios WHERE Username=? AND Password=?''', (username, password))

            self.verify_data = self.cursor.fetchone() # Percorre a tabela de usuários

            if self.verify_data:
                messagebox.showinfo(title='Aviso', message=f'Bem-vindo ao sistema PetCare {username}!')
                self.clean_entry_login()
            else:
               messagebox.showerror(title='Erro', message='Falha ao efetuar o login,\ndados não encontrados.\nCaso não possua uma conta,\ncadastre-se antes.')
               self.desconnect_db
        except Exception as e:
            if hasattr(self, 'conn'):
                self.desconnect_db()
                messagebox.showerror(title='Erro', message=f'Erro ao conectar ao banco de dados: {str(e)}')
            



class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial() # faz com que a função seja executava sempre
        self.tela_de_login()
        self.create_table()

    # Configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("PetCare")
        self.resizable(False, False) # impossibilita a pessoa de mudar o tamanho da janela, ver como faria pra fazer se ajustar pra tela cheia
        #self._fg_color='pink'

    def tela_de_login(self):

        # Trabalhando com as imagens
        self.img = PhotoImage(file='cat1.png')
        self.lb_img = ctk.CTkLabel(
            self,
            text=None,
            image=self.img
            ) # self pq fica na tela principal
        self.lb_img.grid(row=1, column=0, padx=10) # padx é o espaço dos lados no eixo x

        self.update_main_title('Faça seu login ou \ncadastre-se na PetCare')

        # Título da plataforma
        self.title_label = ctk.CTkLabel(
            self,
            text='Faça seu login ou \ncadastre-se na PetCare',
            font=('Century Gothic', 14, 'bold'),
        )
        self.title_label.grid(row=0, column=0, pady=10, padx=10)

        # Criar o frame do formulário de login
        self.frame_login = ctk.CTkFrame(
            self,
            width=350,
            height=380,
            #fg_color='black'
            )
        self.frame_login.place(x=350, y=10)
        

        # Colocando widgets dentro do frame - formulário de login
        self.lb_title = ctk.CTkLabel(
            self.frame_login,
            text='🐾Faça o seu login!',
            font=('Century Gothic', 22, 'bold'),
            text_color='white'
        )
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(
            self.frame_login,
            width=300,
            placeholder_text='Nome de usuário..',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color='pink'
            )
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.password_login_entry = ctk.CTkEntry(
            self.frame_login,
            width=300,
            placeholder_text='Senha..',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color='pink',
            show='*'
            )
        self.password_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.check_password = ctk.CTkCheckBox(
            self.frame_login,
            text='Ver senha',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            border_color='pink',
            command=self.toggle_password
            )
        self.check_password.grid(row=3, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(
            self.frame_login,
            width=300,
            text='Login',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color='pink', # cor do botão
            hover_color='white', # cor do botão quando passa o mouse em cima 
            text_color='black',
            border_width=2,
            border_color='white',
            #command=self.clean_entry_login, # talvez tenha que tirar
            command=self.verify_login
            )
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(
            self.frame_login,
            text='Não possui conta?\nCadastre-se clicando no botão abaixo:',
            font=('Century Gothic', 12, 'bold')
            )
        self.span.grid(row=5, column=0, padx=10, pady=10)

        self.register_button = ctk.CTkButton(
            self.frame_login,
            text='Cadastre-se',
            font=('Century Gothic', 14, 'bold'),
            corner_radius=20,
            fg_color='pink',
            hover_color='white',
            text_color='black',
            border_width=2,
            border_color='white',
            command=self.register_screen
        )
        self.register_button.grid(row=6, column=0, padx=10, pady=10)

    def update_main_title(self, text):
        if hasattr(self, 'title_label'):
            if self.title_label.winfo_exists():
                self.title_label.configure(text=text)
            else:
                self.title_label = ctk.CTkLabel(
                    self,
                    text=text,
                    font=('Century Gothic', 14, 'bold'),
                )
                self.title_label.grid(row=0, column=0, padx=10, pady=10)
        else:
            self.title_label = ctk.CTkLabel(
                self,
                text=text,
                font=('Century Gothic', 14, 'bold'),
            )
            self.title_label.grid(row=0, column=0, padx=10, pady=10)


    def register_screen(self): # Fazer mudar o texto de cima e a imagem
        # Remover o formulário de login
        self.frame_login.place_forget()

        # Criar o frame do formulário de login
        self.update_main_title('Realize o cadastro para começar\nsua jornada na PetCare!')
        self.frame_register = ctk.CTkFrame(
            self,
            width=350,
            height=380,
            #fg_color='black'
            )
        self.frame_register.place(x=350, y=10)

        # Criando o título
        self.lb_title = ctk.CTkLabel(
            self.frame_register,
            text='🐾Faça o seu cadastro!',
            font=('Century Gothic', 22, 'bold'),
            text_color='white'
            )
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        # Criar os widgets da tela de cadastro
        self.username_register_entry = ctk.CTkEntry(
            self.frame_register,
            width=300,
            placeholder_text='Nome de usuário..',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color='pink'
            )
        self.username_register_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_register_entry = ctk.CTkEntry(
            self.frame_register,
            width=300,
            placeholder_text='E-mail..',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color='pink'
            )
        self.email_register_entry.grid(row=2, column=0, padx=10, pady=5)

        self.password_register_entry = ctk.CTkEntry(
            self.frame_register,
            width=300,
            placeholder_text='Senha..',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color='pink',
            show='*'
            )
        self.password_register_entry.grid(row=3, column=0, padx=10, pady=5)

        self.password_confirm_entry_register = ctk.CTkEntry(
            self.frame_register,
            width=300,
            placeholder_text='Confirme a senha..',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            border_color='pink',
            show='*'
            )
        self.password_confirm_entry_register.grid(row=4, column=0, padx=10, pady=5)

        self.check_register_password = ctk.CTkCheckBox(
            self.frame_register,
            text='Ver senha',
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            border_color='pink',
            command=self.toggle_password_register
            )
        self.check_register_password.grid(row=5, column=0, padx=10, pady=5)

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
            command=self.tela_de_login
            )
        self.btn_back_login.grid(row=7, column=0, padx=10, pady=5)

    def clean_entry_register(self): # ta apagando o texto da caixa aparentemente
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

    def toggle_password_register(self):
        if self.check_register_password.get():
            self.password_register_entry.configure(show='')
            self.password_confirm_entry_register.configure(show='')
        else:
            self.password_register_entry.configure(show='*')
            self.password_confirm_entry_register.configure(show='*')


if __name__ == '__main__':
    app = App()
    app.mainloop()

