from __future__ import annotations
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()

    # Configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("PetCare")
        self.resizable(False, False)
        self.configure(fg_color='#FFE4E1')  # Fundo rosa claro

    def tela_de_login(self):
        # Trabalhando com as imagens - USANDO CTkImage para evitar warning
        try:
            from PIL import Image
            self.img = ctk.CTkImage(
                light_image=Image.open("cat1.png"),
                dark_image=Image.open("cat1.png"),
                size=(300, 300)
            )
            self.lb_img = ctk.CTkLabel(
                self,
                text=None,
                image=self.img
            )
        except:
            # Se não encontrar imagem, mostra um texto
            self.lb_img = ctk.CTkLabel(
                self,
                text="🐾 PetCare 🐶",
                font=('Century Gothic', 24, 'bold'),
                text_color='#FF69B4'
            )
        
        self.lb_img.grid(row=1, column=0, padx=10)

        # Título da plataforma
        self.title = ctk.CTkLabel(
            self,
            text='Faça seu login ou \ncadastre-se na PetCare',
            font=('Century Gothic', 14, 'bold'),
            text_color='#FF69B4'
        )
        self.title.grid(row=0, column=0, pady=10, padx=10)

        # Criar o frame do formulário de login
        self.frame_login = ctk.CTkFrame(
            self,
            width=350,
            height=380,
            fg_color='white',
            border_width=2,
            border_color='#FF69B4',
            corner_radius=20
        )
        self.frame_login.place(x=350, y=10)

        # Colocando widgets dentro do frame - formulário de login
        self.lb_title = ctk.CTkLabel(
            self.frame_login,
            text='Faça o seu login!',
            font=('Century Gothic', 22, 'bold'),
            text_color='#FF69B4'
        )
        self.lb_title.grid(row=0, column=0, padx=10, pady=20)

        # Campo de usuário
        self.username_login_entry = ctk.CTkEntry(
            self.frame_login,
            width=300,
            placeholder_text='Nome de usuário..',
            font=('Century Gothic', 16),
            corner_radius=15,
            border_color='#FFB6C1',
            border_width=2,
            fg_color='#FFF5F5'
        )
        self.username_login_entry.grid(row=1, column=0, padx=25, pady=10)

        # Frame para senha + botão de olho
        self.password_container = ctk.CTkFrame(
            self.frame_login, 
            fg_color='transparent',
            height=40
        )
        self.password_container.grid(row=2, column=0, padx=25, pady=10)

        # Campo de senha
        self.password_login_entry = ctk.CTkEntry(
            self.password_container,
            width=265,  # Reduzido para caber o botão
            placeholder_text='Senha..',
            font=('Century Gothic', 16),
            corner_radius=15,
            border_color='#FFB6C1',
            border_width=2,
            fg_color='#FFF5F5',
            show='*'
        )
        self.password_login_entry.pack(side='left', padx=(0, 5))

        # Botão de olho para mostrar/ocultar senha
        self.btn_show_password = ctk.CTkButton(
            self.password_container,
            width=35,
            height=35,
            text='👁️',
            font=('Century Gothic', 14),
            corner_radius=17,
            fg_color='#FF69B4',
            hover_color='#FF1493',
            border_width=2,
            border_color='#FFB6C1',
            command=self.toggle_password_login
        )
        self.btn_show_password.pack(side='left')

        # Botão de login
        self.btn_login = ctk.CTkButton(
            self.frame_login,
            width=300,
            height=45,
            text='Login',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color='#FF69B4',
            hover_color='#FF1493',
            text_color='white',
            border_width=2,
            border_color='white'
        )
        self.btn_login.grid(row=3, column=0, padx=25, pady=15)

        # Texto para cadastro
        self.span = ctk.CTkLabel(
            self.frame_login,
            text='Não possui conta?\nCadastre-se clicando no botão abaixo:',
            font=('Century Gothic', 12),
            text_color='#FF69B4'
        )
        self.span.grid(row=4, column=0, padx=10, pady=10)

        # Botão para ir para cadastro
        self.register_button = ctk.CTkButton(
            self.frame_login,
            width=200,
            height=35,
            text='Cadastre-se',
            font=('Century Gothic', 14, 'bold'),
            corner_radius=15,
            fg_color='white',
            hover_color='#FFF5F5',
            text_color='#FF69B4',
            border_width=2,
            border_color='#FF69B4',
            command=self.register_screen
        )
        self.register_button.grid(row=5, column=0, padx=10, pady=10)

    def toggle_password_login(self):
        """Alterna visibilidade da senha na tela de login"""
        if self.password_login_entry.cget('show') == '*':
            # Mostrar senha
            self.password_login_entry.configure(show='')
            self.btn_show_password.configure(text='🙈', fg_color='#FF1493')
        else:
            # Ocultar senha
            self.password_login_entry.configure(show='*')
            self.btn_show_password.configure(text='👁️', fg_color='#FF69B4')

    def register_screen(self):
        """Abre a tela de cadastro"""
        # Remover o formulário de login
        self.frame_login.place_forget()
        self.title.configure(text='Cadastre-se na PetCare')

        # Atualizar imagem (opcional)
        try:
            self.lb_img.configure(image=ctk.CTkImage(
                light_image=Image.open("dog1.png") if Image else None,
                dark_image=Image.open("dog1.png") if Image else None,
                size=(300, 300)
            ))
        except:
            self.lb_img.configure(text="🐶 Cadastre-se 🐾")

        # Criar o frame do formulário de cadastro
        self.frame_register = ctk.CTkFrame(
            self,
            width=350,
            height=380,
            fg_color='white',
            border_width=2,
            border_color='#FF69B4',
            corner_radius=20
        )
        self.frame_register.place(x=350, y=10)

        # Título
        self.lb_title_register = ctk.CTkLabel(
            self.frame_register,
            text='Faça o seu cadastro!',
            font=('Century Gothic', 22, 'bold'),
            text_color='#FF69B4'
        )
        self.lb_title_register.grid(row=0, column=0, padx=10, pady=20)

        # Campos de cadastro
        campos = [
            ('Nome de usuário..', 'username_register_entry'),
            ('E-mail..', 'email_register_entry'),
            ('Senha..', 'password_register_entry'),
            ('Confirme a senha..', 'password_confirm_entry')
        ]

        for i, (placeholder, attr_name) in enumerate(campos, 1):
            entry = ctk.CTkEntry(
                self.frame_register,
                width=300,
                placeholder_text=placeholder,
                font=('Century Gothic', 16),
                corner_radius=15,
                border_color='#FFB6C1',
                border_width=2,
                fg_color='#FFF5F5'
            )
            
            if 'senha' in placeholder.lower():
                entry.configure(show='*')
            
            entry.grid(row=i, column=0, padx=25, pady=8)
            setattr(self, attr_name, entry)

        # Frame para botão de olho da confirmação de senha
        self.password_confirm_container = ctk.CTkFrame(
            self.frame_register,
            fg_color='transparent',
            height=40
        )
        self.password_confirm_container.grid(row=5, column=0, padx=25, pady=8)

        # Botão de olho para confirmar senha
        self.btn_show_confirm_password = ctk.CTkButton(
            self.password_confirm_container,
            width=35,
            height=35,
            text='👁️',
            font=('Century Gothic', 14),
            corner_radius=17,
            fg_color='#FF69B4',
            hover_color='#FF1493',
            border_width=2,
            border_color='#FFB6C1',
            command=self.toggle_password_confirm
        )
        self.btn_show_confirm_password.pack(side='right', padx=(5, 0))

        # Botão de cadastrar
        self.btn_register = ctk.CTkButton(
            self.frame_register,
            width=300,
            height=45,
            text='Cadastrar',
            font=('Century Gothic', 16, 'bold'),
            corner_radius=20,
            fg_color='#FF69B4',
            hover_color='#FF1493',
            text_color='white',
            border_width=2,
            border_color='white'
        )
        self.btn_register.grid(row=6, column=0, padx=25, pady=15)

        # Botão para voltar ao login
        self.btn_back_login = ctk.CTkButton(
            self.frame_register,
            width=200,
            height=35,
            text='Voltar ao Login',
            font=('Century Gothic', 14, 'bold'),
            corner_radius=15,
            fg_color='white',
            hover_color='#FFF5F5',
            text_color='#FF69B4',
            border_width=2,
            border_color='#FF69B4',
            command=self.back_to_login
        )
        self.btn_back_login.grid(row=7, column=0, padx=10, pady=10)

    def toggle_password_confirm(self):
        """Alterna visibilidade da senha de confirmação"""
        if self.password_confirm_entry.cget('show') == '*':
            # Mostrar ambas as senhas
            self.password_register_entry.configure(show='')
            self.password_confirm_entry.configure(show='')
            self.btn_show_confirm_password.configure(text='🙈', fg_color='#FF1493')
        else:
            # Ocultar ambas as senhas
            self.password_register_entry.configure(show='*')
            self.password_confirm_entry.configure(show='*')
            self.btn_show_confirm_password.configure(text='👁️', fg_color='#FF69B4')

    def back_to_login(self):
        """Volta para a tela de login"""
        # Remover tela de cadastro
        self.frame_register.place_forget()
        
        # Restaurar título original
        self.title.configure(text='Faça seu login ou \ncadastre-se na PetCare')
        
        # Restaurar imagem original
        try:
            self.lb_img.configure(image=ctk.CTkImage(
                light_image=Image.open("cat1.png"),
                dark_image=Image.open("cat1.png"),
                size=(300, 300)
            ))
        except:
            self.lb_img.configure(text="🐾 PetCare 🐶")
        
        # Mostrar tela de login novamente
        self.frame_login.place(x=350, y=10)

if __name__ == "__main__":
    # Configurar aparência
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Executar aplicação
    app = App()
    app.mainloop()