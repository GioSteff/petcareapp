# Para ver os cadastros criar uma segunda tela onde se acessa por um botão "ver pets cadastrados"
# Fazer com que a foto fique maior e transparente, arredondar os cantos da parte rosa, fazer com o que o botão de saltar foto faz seja realizado no final em salvar cadastro no botão que vai ter no fim da janela
# Conferir se realmente salva a imagem no banco de dados pq aparentemente o próprio baco de dados ta vazio e antes n estava


from tkinter import *
from tkinter import Tk, StringVar, ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import sqlite3 as lite
import customtkinter as ctk
import backcadastropet
from tkcalendar import Calendar, DateEntry
from tkinter import Toplevel
from datetime import datetime
import tkinter as tk
from io import BytesIO
import re

# Cores
w = 'white'
p = 'pink'
b = 'black'
fundo = '#242424'
entradas = '#343638'
escrita = '#9E9E9E'

# Criando janela
windowcad = Tk()
windowcad.title('Cadastro Pet')
windowcad.geometry('412x917')
windowcad.configure(background=fundo)
windowcad.resizable(width=FALSE, height=FALSE)

style = ttk.Style(windowcad)
style.theme_use('clam') # testar outros modos e explorar como personalizar o clam

# Criando frames da primeira tela
# Frame rosa + foto do pet

frame1 = ctk.CTkFrame(
    windowcad,
    width=380,
    height=200,
    fg_color=p,
    corner_radius=20
)
frame1.place(x=16, y=40)

# Função para criar imagem circular

image_path = None
imagem_tk = None
especie_combo = None

def create_image_circular(path, size=150):
    img = Image.open(path).resize((size, size))
    img = img.convert('RGBA')

    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    img.putalpha(mask)

    return ImageTk.PhotoImage(img)

# Salvar imagem no banco de dados

# def save_photo(path):
#     con = lite.connect('cadastros_pet.db')
#     cur = con.cursor()

#     cur.execute('''
#         INSERT INTO cadastro (imagem)
#         VALUES (?)
#     ''', (path,))

#     con.commit() # salva dados
#     con.close()

# Carregar imagem na tela

def load_image(path):
    global imagem_tk
    global image_path
    image_path = path
    imagem_tk = create_image_circular(path, size=150)
    label_imagem.configure(image=imagem_tk)

# Escolher nova imagem

def chance_image():
    path = filedialog.askopenfilename(
        filetypes=[('Imagens', '*.png *.jpg *.jpeg')]
    )

    if path:
        load_image(path)

# Imagem padrão

imagem_tk = create_image_circular('fotopadrao.png') # foto padrão

label_imagem = Label(windowcad, image=imagem_tk, bg=p, bd = 0)
label_imagem.place(x=131, y=50)

# Botão

buttonfoto = ctk.CTkButton(
    frame1,
    text='Carregar foto',
    command=chance_image,
    width=50,
    font=('Century Gothic', 10, 'bold'),
    corner_radius=20,
    fg_color='pink', # cor do botão
    hover_color='white', # cor do botão quando passa o mouse em cima 
    text_color='black',
    border_width=1,
    border_color='white',
)
buttonfoto.place(x=144, y=168)

# Criando frame com os campos para cadastro das informações

frame2 = ctk.CTkFrame(
    windowcad,
    width=380,
    height=580,
    fg_color=fundo, # mudar pra fundo
    corner_radius=20
)
frame2.place(x=16, y=250)

# Criando campos

y_pos = 20
fields = []

#Nome1 - dar erro caso insira números ou um nome com meno de 3 letras
entry_name = ctk.CTkEntry(
     frame2,
     placeholder_text='Nome*',
     font=('Century Gothic', 16, 'bold'),
     width=380,
     height=70,
     corner_radius=20,
     border_color=p,
     fg_color=entradas,
     text_color=escrita
)
entry_name.grid(row=1, column=0, padx=0, pady=(30,15))

#Gênero2 
#Fêmea
entry_femea = ctk.CTkButton(
     frame2,
     text='Fêmea',
     font=('Century Gothic', 16, 'bold'),
     width=160,
     height=70,
     corner_radius=20,
     fg_color=entradas,
     text_color=escrita,
     border_width=2,
     border_color=p,
     hover_color=p,
     command=lambda: select_gender('Fêmea')
)
entry_femea.grid(row=2, column=0, padx=(180,5), pady=15)

#Macho
entry_macho = ctk.CTkButton(
     frame2,
     text='Macho',
     font=('Century Gothic', 16, 'bold'),
     width=160,
     height=70,
     corner_radius=20,
     border_width=2,
     border_color=p,
     fg_color=entradas,
     text_color=escrita,
     hover_color=p,
     command=lambda: select_gender('Macho')
)
entry_macho.grid(row=2, column=0, padx=(5,180), pady=15)

#Espécie3 # ver se n daria para transformar em uma caixa que abre com opçoes

# style = ttk.Style()
# style.theme_use('clam')

# style.configure(
#     'Custom.TCombobox',
#     fieldbackground=entradas,
#     background=entradas,
#     forebackground=escrita,
#     arrowcolor=escrita,
#     bordercolor=p,
#     lightcolor=p,
#     darkcolor=p,
#     selectbackground=p,
#     selectforeground=b
# )

# # Forçar cor do texto
# style.map(
#     'Custom.TCombobox',
#     fieldbackground=[('readonly', entradas), ('disabled', entradas)],
#     foreground=[('focus', escrita), ('!focus', escrita), ('active', escrita)],
#     selectbackground=[('focus', p), ('hover', p)],
#     selectforeground=[('focus', b), ('hover', b)]
#)
especies = ['Cachorro', 'Gato', 'Pássaro', 'Peixe', 'Hamster', 'Coelho', 'Réptil', 'Outro']

especie_combo = ctk.CTkComboBox(
    frame2,
    values=especies,
    font=('Century Gothic', 16, 'bold'),
    width=380,
    height=70,
    corner_radius=20,
    border_width=2,
    border_color=p,
    fg_color=entradas,
    text_color=escrita,
    button_color=p,
    button_hover_color=w,
    dropdown_fg_color=entradas,
    dropdown_text_color=escrita,
    dropdown_hover_color=p,
    state='readonly'
)
especie_combo.grid(row=3, column=0, padx=0, pady=15)
especie_combo.set('Espécie')

# entry_species = ctk.CTkEntry(
#      frame2,
#      placeholder_text='Espécie',
#      font=('Century Gothic', 16, 'bold'),
#      width=380,
#      height=70,
#      corner_radius=20,
#      border_color=p,
#      fg_color=entradas,
#      text_color=escrita
# )
# entry_species.grid(row=3, column=0, padx=0, pady=15)

# #Idade4 - dar erro se colocar letras, número negativos ou mt absurdos 
entry_age = ctk.CTkEntry(
     frame2,
     placeholder_text='Idade',
     font=('Century Gothic', 16, 'bold'),
     width=380,
     height=70,
     corner_radius=20,
     border_color=p,
     fg_color=entradas,
     text_color=escrita
)
entry_age.grid(row=4, column=0, padx=0, pady=15)

# #Data_Nascimento5 
# Tentar fazer com que bata com a idade, futuramente transferir isto para o cadastro mais avançado 
# Fazer com que de para mudar depois de selecionado pela primeira vez
# frame_data = tk.Frame(frame2, bg=fundo)
# frame_data.grid(row=5, column=0, padx=0, pady=10)

# label_date = ctk.CTkLabel(
#     frame_data,
#     text='Aniversário',
#     font=('Century Gothic', 14, 'bold'),
#     text_color=escrita
# )
# label_date.pack()

# entry_birthday= DateEntry(
#      frame_data,
#      width=15,
#      background='pink',
#      foreground='white',
#      borderwidth=2,
#      date_pattern='dd/mm/yyyy',
#      locale='pt_BR',
#      font=('Century Gothic', 14, 'bold')
# )
# entry_birthday.pack(side=tk.LEFT)

# #Raça6 - ver se n daria para transformar em uma caixa que abre com opçoes
entry_race = ctk.CTkEntry(
     frame2,
     placeholder_text='Raça',
     font=('Century Gothic', 16, 'bold'),
     width=380,
     height=70,
     corner_radius=20,
     border_color=p,
     fg_color=entradas,
     text_color=escrita
)
entry_race.grid(row=6, column=0, padx=0, pady=15)

# #Microship7 - dar erro caso seja inserido algo fora do padrão de um microship
# entry_microchip= ctk.CTkEntry(
#      frame2,
#      placeholder_text='Microchip',
#      font=('Century Gothic', 16, 'bold'),
#      width=380,
#      height=60,
#      corner_radius=20,
#      border_color=p,
#      fg_color=entradas,
#      text_color=escrita
# )
# entry_microchip.grid(row=7, column=0, padx=0, pady=10)


# Criando botão para cadastrar 

def create_table():
    con = lite.connect('cadastros_pet.db')
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cadastro (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          nome TEXT,
          genero TEXT,
          especie TEXT,
          idade INTEGER,
          raca TEXT,
          imagem BLOB,
          microchip TEXT,
          data_nascimento TEXT,
          data_adocao TEXT,
          contato TEXT,
          castrado TEXT
      )
    ''')
    con.commit()
    con.close()

create_table()

def save_pet():
    global image_path, imagem_tk

    nome = entry_name.get()
    nome = nome.capitalize()

    genero = selected_gender.get()
    especie = especie_combo.get()
    idade = entry_age.get()
    #data_nascimento = entry_birthday.get()
    raca = entry_race.get()
    #microchip = entry_microchip.get()

    # Campos vazios por enquanto:
    microchip = ''
    data_nascimento = ''
    data_adocao = ''
    contato = ''
    castrado = ''

    if not all([nome, genero, especie, idade, raca]):
        messagebox.showwarning(title='', message='Preencha as informações para continuar.')
        return
    
    if not genero:
        messagebox.showwarning(title='', message='Gênero não selecionado.') # botar mensagem certo
        return
    
    if not image_path:
        messagebox.showwarning(title='', message='Carregue uma foto de seu pet.')
        return
    
    if any(char.isdigit() for char in nome):
        messagebox.showerror(title='', message='Insira um nome válido.')
        return
    
    if len(nome) < 3:
        messagebox.showerror(title='', message='Insira um nome com pelo menos 3 letras.')
        return
    
    if len(raca) < 3:
        messagebox.showerror(title='', message='Insira uma raça existente.')
        return
    
    if any(char.isdigit() for char in raca):
        messagebox.showerror(title='', message='Insira uma raça existente.')
        return
    
    # microchip = microchip.strip()

    # if len(microchip) != 15:
    #     messagebox.showerror(title='', message='O código do microchip deve incluir 15 números.')
    #     return

    # if not microchip.isdigit():
    #     messagebox.showerror('O código do microchip não deve incluir letras.')
    #     return
    
    try:
        idade = int(idade)
        if idade < 0:
            messagebox.showerror(title='', message='Insira uma idade válida.')
            return
        if idade > 30:
            messagebox.showerror(title='', message='Idade inválida')
            return
    except ValueError:
        messagebox.showerror(title='', message='Insira um número inteiro válido para a idade.')
        return
    
    try:
        # Conectar ao banco
        con = lite.connect('cadastros_pet.db')
        cur = con.cursor()

        # Ler a imagem como binário
        with open(image_path, 'rb') as file:
            blob_image = file.read()

        # Inserir todos os dados
        cur.execute('''
            INSERT INTO cadastro (
                    nome, genero, especie, idade, raca, imagem, microchip, data_nascimento, data_adocao, contato, castrado
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        ''', (nome, genero, especie, idade, raca, blob_image, microchip, data_nascimento, data_adocao, contato, castrado))

        con.commit()
        con.close()

        messagebox.showinfo(title='', message='Pet cadastrado com sucesso.')

        # Limpar campos
        entry_name.delete(0, END)
        entry_age.delete(0, END)
        entry_race.delete(0, END)
        #entry_microchip.delete(0, END)
        #entry_birthday.insert(0, datetime.now().strftime('%d/%m/%Y'))

        # Resetar genero
        selected_gender.set('')
        entry_macho.configure(fg_color=entradas, text_color=escrita)
        entry_femea.configure(fg_color=entradas, text_color=escrita)

        image_path = None
        imagem_tk = create_image_circular('fotopadrao.png', size=150)
        label_imagem.configure(image=imagem_tk)

        # Resetar espécie
        especie_combo.set('')

    except Exception as e:
        messagebox.showerror('Erro', f'Erro: {e}')
        

selected_gender = StringVar(value='')

def select_gender(gender):
    selected_gender.set(gender)
    # Fazer o botão selecionado mudar de cor:
    if gender == 'Macho':
        entry_macho.configure(fg_color=p, text_color=escrita)
        entry_femea.configure(fg_color=entradas, text_color=escrita)
    else:
        entry_femea.configure(fg_color=p, text_color=escrita)
        entry_macho.configure(fg_color=entradas, text_color=escrita)


buttonregistrar = ctk.CTkButton(
    windowcad,
    text='Registrar',
    command=save_pet,
    width=380,
    height=70,
    font=('Century Gothic', 20, 'bold'),
    corner_radius=20,
    fg_color='pink', # cor do botão
    hover_color='white', # cor do botão quando passa o mouse em cima 
    text_color='black',
    border_width=2,
    border_color=p
)
buttonregistrar.place(x=16, y=780)

# Função para ver pets (nova tela)
def registered_pets():
    window_pets=Toplevel(windowcad)
    window_pets.title('Pets Cadastrados')
    window_pets.geometry('500x600')
    window_pets.configure(background=fundo)
    window_pets.resizable(FALSE, FALSE)

    # Focar na nova janela
    window_pets.focus_set()
    windowcad.withdraw()

    # Quando fechar janela mostrar a principal dnv
    def on_closing():
        window_pets.destroy()
        windowcad.deiconify() # por causa do withdraw

    window_pets.protocol('WM_DELETE_WINDOW', on_closing)

    frame_pets = ctk.CTkFrame(
        window_pets,
        width=450,
        height=550,
        fg_color=p,
        corner_radius=20
    )
    frame_pets.place(x=25, y=25)

    ctk.CTkLabel(
        frame_pets,
        text='PETS CADASTRADOS',
        font=('Century Gothic', 20, 'bold'),
        text_color=b,
    ).place(x=130, y=15)

    # Botão voltar
    ctk.CTkButton(
        frame_pets,
        text='Cadastrar novo pet',
        command=on_closing,
        width=100,
        height=30,
        font=('Century Gothic', 14, 'bold'),
        corner_radius=20,
        fg_color=p,
        hover_color=w,
        border_width=2,
        border_color=w,
        text_color=b
    ).place(x=145, y=45)

    # Lista de pets
    frame_list = Frame(frame_pets, bg=p)
    frame_list.place(x=20, y=80, width=410, height=440)

    scrollbar = Scrollbar(frame_list)
    scrollbar.pack(side=RIGHT, fill=Y)

    list_pets = Listbox(
        frame_list,
        yscrollcommand=scrollbar.set,
        font=('Century Gothic', 12, 'bold'),
        bg=fundo,
        fg=w,
        selectbackground=p
    )
    list_pets.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=list_pets.yview)

    try:
        con = lite.connect('cadastros_pet.db')
        cur = con.cursor()
        cur.execute('SELECT id, nome, especie, idade FROM cadastro')
        pets = cur.fetchall()
        con.close()

        if pets:
            for pet in pets:
                list_pets.insert(END, f'ID {pet[0]}: {pet[1]} - {pet[2]} - {pet[3]} anos') 
        else:
            list_pets.insert(END, 'Nenhum pet cadastrado')
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao carregar pets: {e}')

    # Função para quand clicar duas vezes no pet
    def on_pet_select(event):
        try:
            # Pega o item selecionado
            selection = list_pets.curselection()
            if not selection:
                return
            
            # Pegar o texto do item selecionado
            selected_text = list_pets.get(selection[0])

            # Extrair o ID do pet
            if selected_text.startswith('ID '):
                pet_id = int(selected_text.split(':')[0].replace('ID ', ''))

                window_pets.destroy()
                #windowcad.deiconify()

                show_pet_details(pet_id) # chama a fun externa
        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao selecionar pet: {e}')
             
    # Vincular evento de duplo clique
    list_pets.bind('<Double-Button-1>', on_pet_select)

# Função para mostrar detalhes do pet
def show_pet_details(pet_id):
    try:
        # Buscar dados do pet no banco
        con = lite.connect('cadastros_pet.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM cadastro WHERE id = ?', (pet_id,))
        pet = cur.fetchone()
        con.close()

        if not pet:
            messagebox.showerror('Erro', 'Pet não encontrado')
            return
        
        # Janela de detalhes
        details_window = Toplevel(windowcad)
        details_window.title(f'{pet[1]}')
        details_window.configure(background=fundo)
        details_window.geometry('450x700')
        details_window.resizable(FALSE, FALSE)

        # Focar na nova janela
        details_window.focus_set()

        # Fechar corretamente
        def close_details():
            details_window.destroy()
        
        details_window.protocol('WM_DELETE_WINDOW', close_details)

        # Frame principal
        main_frame = ctk.CTkFrame(
            details_window,
            width=400,
            height=650,
            fg_color=p,
            corner_radius=20
        )
        main_frame.place(x=25, y=25)

        # Título
        ctk.CTkLabel(
            main_frame,
            text=f'🐾FICHA DO PET🐾',
            font=('Helvetica', 30, 'bold'),
            text_color=b,
        ).place(x=60, y=20)

        # Frame para a foto (circular)
        if len(pet) > 6 and pet[6]: # Se tem imagem (indice 0 porque começa do 0:id, nome, genero, especie, idade, data_nascimento, raca, microship, imagem)
            try:
                # Converter blob para imagem 
                image_data = BytesIO(pet[6])
                img = Image.open(image_data)

                # Redimensionar e fazer circular
                img = img.resize((150,150), Image.LANCZOS)
                img = img.convert('RGBA')

                # Criar máscara circular 
                mask = Image.new('L', (150,150), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0,0,150,150), fill=255)

                # Aplicar máscara com transparência  
                img.putalpha(mask)

                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(img)

                # Label para a foto
                photo_label = Label(main_frame, image=photo, bg=p, bd=0)
                photo_label.image = photo # Manter referência
                photo_label.place(x=125, y=70)
            except Exception as e:
                messagebox.showerror(title='Erro', message='Erro ao carregar imagem: {e}')
                default_img = create_image_circular('fotopadrao.png', size=150)
                photo_label = Label(main_frame, image=default_img, bg=p, bd=0)
                photo_label.image = default_img
                photo_label.place(x=125, y=70)
        else:
            # Foto padrão se não tiver imagem
            default_img = create_image_circular('fotopadrao.png', size=150)
            photo_label = Label(
                main_frame,
                image=default_img,
                bg=p,
                bd=0
                )
            photo_label.image = default_img
            photo_label.place(x=125, y=70)

        # Frame para informaçõe:
        info_frame = ctk.CTkFrame(
            main_frame,
            width=350,
            height=400,
            fg_color=fundo,
            corner_radius=20
        )
        info_frame.place(x=25, y=230)

        # Informações do pet
        info_y = 15
        info_spacing = 30

        # Nome
        ctk.CTkLabel(
            info_frame,
            text='NOME:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[1],
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=100, y=info_y)
        info_y += info_spacing

        # Gênero
        ctk.CTkLabel(
            info_frame,
            text='GÊNERO:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[2],
            font=('Century Gothic', 14, 'bold'),
            text_color=w,
        ).place(x=100, y=info_y)
        info_y += info_spacing

        # Espécie
        ctk.CTkLabel(
            info_frame,
            text='ESPÉCIE:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[3],
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=100, y=info_y)
        info_y += info_spacing

        # Idade
        ctk.CTkLabel(
            info_frame,
            text='IDADE:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=f'{pet[4]} anos',
            font=('Century Gothic', 14, 'bold'),
            text_color=w,
        ).place(x=100, y=info_y)
        info_y += info_spacing

        # Raca
        ctk.CTkLabel(
            info_frame,
            text='RAÇA:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[5],
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=100, y=info_y)
        info_y += info_spacing

        # Microchip
        ctk.CTkLabel(
            info_frame,
            text='MICROCHIP:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[7] if pet[7] else '',
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=120, y=info_y)
        info_y += info_spacing

        # Data de nascimento 
        ctk.CTkLabel(
            info_frame,
            text='NASCIMENTO:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[8] if pet[8] else '',
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=120, y=info_y)
        info_y += info_spacing

        # Data de adoção 
        ctk.CTkLabel(
            info_frame,
            text='ADOÇÂO:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[9] if pet[9] else '',
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=120, y=info_y)
        info_y += info_spacing

        # Número de contato
        ctk.CTkLabel(
            info_frame,
            text='NÚMERO:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[10] if pet[10] else '',
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=120, y=info_y)
        info_y += info_spacing

        # Castrado? 
        ctk.CTkLabel(
            info_frame,
            text='CASTRADO:',
            font=('Century Gothic', 12, 'bold'),
            text_color=escrita
        ).place(x=20, y=info_y)

        ctk.CTkLabel(
            info_frame,
            text=pet[11] if pet[11] else '',
            font=('Century Gothic', 14, 'bold'),
            text_color=w
        ).place(x=120, y=info_y)
        info_y += info_spacing

        # Botão fechar
        ctk.CTkButton(
            main_frame,
            text='X', # mudar
            command=lambda: [details_window.destroy(), registered_pets()], 
            width=40,
            height=40,
            font=('Century Gothic', 18, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=b
        ).place(x=25, y=180) #x75

        # Botão para apagar pet selecionado com confirmação
        ctk.CTkButton(
            info_frame,
            text='Deletar', # mudar
            command=lambda: delete_pet(pet_id, pet[1]),
            width=40,
            height=20,
            font=('Century Gothic', 12, 'bold'),
            corner_radius=20,
            fg_color=w,
            hover_color=p,
            text_color=b,
            border_width=2,
            border_color=w
        ).place(x=145, y=370) 

        # Botão para cadastrar mais opções e alterar antigas
        ctk.CTkButton(
            info_frame,
            text='Editar',
            command=lambda: edit_pet(pet_id, pet),
            width=220,
            height=40,
            font=('Century Gothic', 14, 'bold'),
            corner_radius=20,
            fg_color=p,
            hover_color=w,
            text_color=b,
            border_width=2,
            border_color=p
        ).place(x=66, y=326) 

    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao carregar detalhes: {e}')

# botão para ver pets cadastrados
button_registered_pets = ctk.CTkButton(
    windowcad,
    text='Pets Cadastrados',
    command=registered_pets,
    width=250,
    height=35,
    font=('Century Gothic', 14, 'bold'),
    corner_radius=20,
    fg_color=w,
    hover_color=p,
    text_color=b,
    border_width=1,
    border_color=w
)
button_registered_pets.place(x=85, y=860)

# Função - Janela de cadastro de mais opções e alterar antigas

def delete_pet(pet_id, pet_nome):
    resposta = messagebox.askyesno(
        'Confirmar',
        f'Tem certeza que deseja deletar o registro de {pet_nome}?'
    )

    if resposta:
        try:
            con = lite.connect('cadastros_pet.db')
            cur = con.cursor()
            cur.execute('DELETE FROM cadastro WHERE id = ?', (pet_id,))
            con.commit()
            con.close()

            for widget in windowcad.winfo_children():
                if isinstance(widget, Toplevel) and widget.title() == pet_nome:
                    widget.destroy()
                    break

            messagebox.showinfo('Sucesso', 'Registro do pet deletado')
            registered_pets()

        except Exception as e:
            messagebox.showerror('Erro', f'Erro ao deletar: {e}')


def validar_contato(contato):
    # Formatos aceitos:
    # +XX (XX) XXXXX-XXXX (qualquer código de país)
    # (XX) XXXXX-XXXX
    # XXXXXXXXXXX (só números)

    contato = contato.strip()

    if not contato:
        return True, ''
    
    # Regex para formato +55 (11) 99999-9999
    # \d - qualquer dígito numérico de 0 a 9
    # Regex	O que aceita
    # \d	    7
    # \d\d	    42
    # \d{3}     123
    # \d{10}	1198765432
    # ^   → começo
    # $   → fim
    padrao1 = r'^\+\d{1,3}\s\(\d{2}\)\s\d{4,5}-\d{4}$'
    # Regex para formato (11) 99999-9999
    padrao2 = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    # Regex para formato 1199999-9999 ou 11999999999
    padrao3 = r'^\d{10,13}$'

    if re.match(padrao1, contato):
        return True, contato
    elif re.match(padrao2, contato):
        return True, contato
    elif re.match(padrao3, contato):
        if len(contato) == 13:
            cod_pais = contato[:2]
            ddd = contato[2:4]
            numero = contato[4:]
            if len(numero) == 9:
                return True, f'+{cod_pais} ({ddd}) {numero[:5]}-{numero[5:]}'
            else:
                return True, f'+{cod_pais} ({ddd}) {numero[:4]}-{numero[4:]}'
            
        elif len(contato) == 12:
            cod_pais = contato[:2]
            ddd = contato[2:4]
            numero = contato[4:]
            return True, f'+{cod_pais} ({ddd}) {numero[:4]}-{numero[4:]}'
        
        elif len(contato) == 11:
            ddd = contato[:2]
            numero = contato[2:]
            if len(numero) == 9:
                return True, f'({ddd}) {numero[:5]}-{numero[5:]}'
            else:
                return True, f'({ddd}) {numero[:4]}-{numero[4:]}'
            
        elif len(contato) == 10:
            ddd = contato[:2]
            numero = contato[2:]
            return True, f'({ddd}) {numero[:4]}-{numero[4:]}'
        
    return False, 'Número inválido'

def edit_pet(pet_id, pet_dados):
    global nova_imagem_path
    nova_imagem_path = None
    
    # Fecha a janela de detalhes antes de abrir a edição
    for widget in windowcad.winfo_children():
        if isinstance(widget, Toplevel) and widget.title() != 'Pets Cadastrados':
            widget.destroy()
    # Buscar dados do pet no banco
    con = lite.connect('cadastros_pet.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM cadastro WHERE id = ?', (pet_id,))
    pet = cur.fetchone()
    con.close()

    if not pet:
        messagebox.showerror('Erro', 'Pet não encontrado')
        return
    
    edit_window = Toplevel(windowcad)
    edit_window.title(f'{pet[1]}')
    edit_window.geometry('450x680')
    edit_window.configure(background=fundo)
    edit_window.resizable(FALSE, FALSE)

    def load_new_image(path):
        global nova_imagem_path
        nova_imagem_path = path
        # Mostrar prévia da nova imagem
        img = Image.open(path).resize((60,60), Image.LANCZOS)
        img = img.convert('RGBA')

        # Máscara circular
        mask = Image.new('L', (60,60), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0,60,60), fill=255)
        img.putalpha(mask)

        photo = ImageTk.PhotoImage(img)
        preview_label.config(image=photo)
        preview_label.image = photo

    def choose_new_image():
        path = filedialog.askopenfilename(
            filetypes=[('Imagens', '*.png *.jpg *.jpeg')]
        )
        if path:
            load_new_image(path)

    # Frame principal
    main_frame = ctk.CTkFrame(
        edit_window,
        width=400,
        height=630,
        fg_color=p,
        corner_radius=20
    )
    main_frame.place(x=25, y=25)

    # Título
    ctk.CTkLabel(
        main_frame,
        text=f'✎ EDITAR PET ✎\n{pet[1]}'.upper(),
        font=('Helvetica', 24, 'bold'),
        text_color=b,
    ).place(x=100, y=20)

    # Frame para imagem nova
    frame_image = Frame(main_frame, bg=p)
    frame_image.place(x=110, y=498)

    # Mostrar imagem atual
    try:
        if pet_dados[6]:
            img_data = BytesIO(pet_dados[6])
            img_pil = Image.open(img_data).resize((60,60), Image.LANCZOS)
            img_pil = img_pil.convert('RGBA')

            # Máscara circular
            mask = Image.new('L', (60, 60), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 60, 60), fill=255)
            img_pil.putalpha(mask)

            img_tk = ImageTk.PhotoImage(img_pil)
            preview_label = Label(frame_image, image=img_tk, bg=p, bd=0)
            preview_label.image = img_tk
        else:
            img_padrao = create_image_circular('fotopadrao.png', 60)
            preview_label = Label(frame_image, image=img_padrao, bg=p, bd=0)
            preview_label.image = img_padrao
    except:
        img_padrao = create_image_circular('fotopadrao.png', 60)
        preview_label = Label(frame_image, image=img_padrao, bg=p, bd=0)
        preview_label.image = img_padrao

    preview_label.pack(side=LEFT, padx=5)

    # Botão para trocar imagem
    ctk.CTkButton(
        frame_image,
        text='Atualizar foto',
        command=choose_new_image,
        width=100,
        height=30,
        font=('Century Gothic', 12, 'bold'),
        corner_radius=15,
        fg_color=entradas,
        hover_color=w,
        text_color=escrita
    ).pack(side=LEFT, padx=5)

    # Frame para os campos
    fields_frame = ctk.CTkFrame(
        main_frame,
        width=350,
        height=400,
        fg_color=fundo,
        corner_radius=20
    )
    fields_frame.place(x=25, y=90)

    # Campos de edição
    y_poss = 15
    spacing = 35

    # NOME
    ctk.CTkLabel(
        fields_frame,
        text='Nome:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita
    ).place(x=20, y=y_poss)

    entry_nome = ctk.CTkEntry(
        fields_frame,
        font=('Century Gothic', 14, 'bold'),
        width=200,
        height=25,
        corner_radius=10,
        fg_color=entradas,
        text_color=w
    )
    entry_nome.place(x=140, y=y_poss)
    entry_nome.insert(0, pet_dados[1])
    y_poss += spacing

    # GÊNERO
    ctk.CTkLabel(
        fields_frame,
        text='Gênero:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita
    ).place(x=20, y=y_poss)

    genero_var = StringVar(value=pet_dados[2])

    frame_genero = Frame(fields_frame, bg=fundo)
    frame_genero.place(x=140, y=y_poss)

    ctk.CTkRadioButton(
        frame_genero,
        text='Macho',
        variable=genero_var,
        value='Macho',
        font=('Century Gothic', 12, 'bold'),
        text_color=w,
        fg_color=p
    ).pack(side=LEFT, padx=5)

    ctk.CTkRadioButton(
        frame_genero,
        text='Fêmea',
        variable=genero_var,
        value='Fêmea',
        font=('Century Gothic', 12, 'bold'),
        text_color=w,
        fg_color=p
    ).pack(side=LEFT, padx=5)
    y_poss += spacing

    # ESPÉCIE
    especies = ['Cachorro', 'Gato', 'Pássaro', 'Peixe', 'Hamster', 'Coelho', 'Réptil', 'Outro']

    ctk.CTkLabel(
        fields_frame,
        text='Espécie:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita
    ).place(x=20, y=y_poss)

    especie_combo = ttk.Combobox(
        fields_frame,
        values=especies,
        font=('Century Gothic', 14),
        width=16,
        state='readonly'  # 'readonly' se quiser só selecionar
    )
    especie_combo.place(x=140, y=y_poss)
    especie_combo.set(pet_dados[3])  # valor atual
    y_poss += spacing

    # IDADE
    ctk.CTkLabel(
        fields_frame,
        text='Idade:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita
    ).place(x=20, y=y_poss)

    entry_idade = ctk.CTkEntry(
        fields_frame,
        font=('Century Gothic', 14, 'bold'),
        width=200,
        height=25,
        corner_radius=10,
        fg_color=entradas,
        text_color=w
    )
    entry_idade.place(x=140, y=y_poss)
    entry_idade.insert(0, pet_dados[4])
    y_poss += spacing

    # RAÇA
    ctk.CTkLabel(
        fields_frame,
        text='Raça:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita,
    ).place(x=20, y=y_poss)

    entry_raca = ctk.CTkEntry(
        fields_frame,
        font=('Century Gothic', 14, 'bold'),
        width=200,
        height=25,
        corner_radius=10,
        fg_color=entradas,
        text_color=w
    )
    entry_raca.place(x=140, y=y_poss)
    entry_raca.insert(0, pet_dados[5])
    y_poss += spacing

    # MICROCHIP - incluir restrição de formato de entrada
    ctk.CTkLabel(
        fields_frame,
        text='Microchip:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita,
    ).place(x=20, y=y_poss)

    entry_microchip = ctk.CTkEntry(
        fields_frame,
        font=('Century Gothic', 14, 'bold'),
        width=200,
        height=25,
        corner_radius=10,
        fg_color=entradas,
        text_color=w
    )
    entry_microchip.place(x=140, y=y_poss)
    if len(pet_dados) > 7 and pet_dados[7]:
        entry_microchip.insert(0, pet_dados[7])
    y_poss += spacing

    # NASCIMENTO - mudar pra calendário
    ctk.CTkLabel(
        fields_frame,
        text='Nascimento:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita
    ).place(x=20, y=y_poss)
    
    # Frame para o calendário
    frame_data = tk.Frame(fields_frame, bg=fundo)
    frame_data.place(x=140, y=y_poss)

    entry_birthday= DateEntry(
        frame_data,
        width=16,
        background='pink',
        foreground='white',
        borderwidth=2,
        date_pattern='dd/mm/yyyy',
        locale='pt_BR',
        font=('Century Gothic', 14, 'bold')
    )
    entry_birthday.pack(side=tk.LEFT)

    # Correção bug editar depois de já ter selecionado
    #entry_birthday._top_cal.overrideredirect(False)

    #entry_nascimento.place(x=140, y=y_poss)
    if len(pet_dados) > 8 and pet_dados[8]:
        try:
            data = datetime.strptime(pet_dados[8], '%d/%m/%Y')
            entry_birthday.set_date(data)
        except:
            pass
        
    y_poss += spacing

    # ADOÇÂO - mudar pra calendário
    ctk.CTkLabel(
        fields_frame,
        text='Adoção:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita
    ).place(x=20, y=y_poss)
    
    # Frame para o calendário
    frame_data = tk.Frame(fields_frame, bg=fundo)
    frame_data.place(x=140, y=y_poss)

    entry_adoption= DateEntry(
        frame_data,
        width=16,
        background='pink',
        foreground='white',
        borderwidth=2,
        date_pattern='dd/mm/yyyy',
        locale='pt_BR',
        font=('Century Gothic', 14, 'bold')
    )
    entry_adoption.pack(side=tk.LEFT)

    #entry_adoption._top_cal.overrideredirect(False)
    #entry_nascimento.place(x=140, y=y_poss)
    if len(pet_dados) > 9 and pet_dados[9]:
        try:
            data1 = datetime.strptime(pet_dados[9], '%d/%m/%Y')
            entry_adoption.set_date(data1)
        except:
            pass
    
    y_poss += spacing

    # CONTATO
    ctk.CTkLabel(
        fields_frame,
        text='Contato:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita,
    ).place(x=20, y=y_poss)

    entry_contact = ctk.CTkEntry(
        fields_frame,
        font=('Century Gothic', 14, 'bold'),
        width=200,
        height=25,
        corner_radius=10,
        fg_color=entradas,
        text_color=w
    )
    entry_contact.place(x=140, y=y_poss)
    if len(pet_dados) > 10 and pet_dados[10]:
        entry_contact.insert(0, pet_dados[10])
    y_poss += spacing

    # CASTRADO
    ctk.CTkLabel(
        fields_frame,
        text='Castrado:',
        font=('Century Gothic', 12, 'bold'),
        text_color=escrita,
    ).place(x=20, y=y_poss)

    castrado_var = StringVar(value=pet_dados[11] if len(pet_dados) > 8 and pet_dados[11] else '')

    frame_castrado = Frame(fields_frame, bg=fundo)
    frame_castrado.place(x=140, y=y_poss)

    ctk.CTkRadioButton(
        frame_castrado,
        text='Sim',
        variable=castrado_var,
        value='Sim',
        font=('Century Gothic', 12, 'bold'),
        text_color=w,
        fg_color=p
    ).pack(side=LEFT, padx=5)

    ctk.CTkRadioButton(
        frame_castrado,
        text='Não',
        variable=castrado_var,
        value='Não',
        font=('Century Gothic', 12, 'bold'),
        text_color=w,
        fg_color=p
    ).pack(side=LEFT, padx=5)



    # Função para salvar alterações
    def save_changes(): # completar depois
        try:
            nome = entry_nome.get().capitalize()
            genero = genero_var.get()
            especie = especie_combo.get()
            idade = entry_idade.get()
            raca = entry_raca.get()
            microchip = entry_microchip.get().strip()
            data_nascimento = entry_birthday.get()
            data_adocao = entry_adoption.get()
            contato = entry_contact.get().strip()
            castrado = castrado_var.get()

            # Validações

            valido, resultado  = validar_contato(contato)
            if not valido:
                messagebox.showerror('Erro', resultado)
                return
            if resultado != True:
                contato = resultado # usa a versão formatada

            if not all([nome, genero, especie, idade, raca]):
                messagebox.showwarning(title='', message='Preencha as informações iniciais para continuar.')
                return
            
            if not genero:
                messagebox.showwarning(title='', message='Gênero não selecionado.') # botar mensagem certo
                return
            
            if any(char.isdigit() for char in nome):
                messagebox.showerror(title='', message='Insira um nome válido.')
                return
            
            if len(nome) < 3:
                messagebox.showerror(title='', message='Insira um nome com pelo menos 3 letras.')
                return
            
            if len(raca) < 3:
                messagebox.showerror(title='', message='Insira uma raça existente.')
                return
            
            if any(char.isdigit() for char in raca):
                messagebox.showerror(title='', message='Insira uma raça existente.')
                return
            
            if microchip:
                if len(microchip) != 15:
                    messagebox.showerror(title='', message='O código do microchip deve incluir 15 números.')
                    return
                if not microchip.isdigit():
                    messagebox.showerror('O código do microchip não deve incluir letras.')
                    return
                
            #if contato
            
            try:
                idade = int(idade)
                if idade < 0:
                    messagebox.showerror(title='', message='Insira uma idade válida.')
                    return
                if idade > 30:
                    messagebox.showerror(title='', message='Idade inválida')
                    return
            except ValueError:
                messagebox.showerror(title='', message='Insira um número inteiro válido para a idade.')
                return
        
            con = lite.connect('cadastros_pet.db')
            cur = con.cursor()

            if nova_imagem_path:
                with open(nova_imagem_path, 'rb') as file:
                    blob_image = file.read()

                # Atualiza dados
                cur.execute('''
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
                contato=?,
                castrado=?
                WHERE id=?
                ''', (
                nome,
                genero,
                especie,
                idade,
                raca,
                blob_image,
                microchip,
                data_nascimento,
                data_adocao,
                contato,
                castrado,
                pet_id
                ))
            else:
                # UPDATE sem imagem
                cur.execute('''
                    UPDATE cadastro SET
                    nome=?,
                    genero=?,
                    especie=?,
                    idade=?,
                    raca=?,
                    microchip=?,
                    data_nascimento=?,
                    data_adocao=?,
                    contato=?,
                    castrado=?
                    WHERE id=?
                ''', (
                    nome,
                    genero,
                    especie,
                    idade,
                    raca,
                    microchip,
                    data_nascimento,
                    data_adocao,
                    contato,
                    castrado,
                    pet_id
                ))

            con.commit()
            con.close()

            messagebox.showinfo('Sucesso', 'Pet Atualizado')
            edit_window.destroy()
            for widget in windowcad.winfo_children():
                if isinstance(widget, Toplevel) and widget.title() != 'Pets Cadastrados':
                    widget.destroy()
            show_pet_details(pet_id)
        
        except Exception as e:
           messagebox.showerror('Erro', f'Erro ao salvar: {e}')

    # Botões
    ctk.CTkButton(
        main_frame,
        text='SALVAR',
        command=save_changes,
        width=150,
        height=35,
        font=('Century Gothic', 14, 'bold'),
        corner_radius=20,
        fg_color=entradas,
        hover_color=w,
        text_color=escrita,
        #border_width=2,
        #border_color=b
    ).place(x=125, y=560)

    ctk.CTkButton(
        main_frame,
        text='CANCELAR',
        command=lambda: [edit_window.destroy(), show_pet_details(pet_id)],
        width=80,
        height=25,
        font=('Century Gothic', 12, 'bold'),
        corner_radius=20,
        fg_color=w,
        text_color=escrita,
        #border_width=2,
        #border_color=b,
        hover_color=entradas,
    ).place(x=155, y=598)



# Verificar se não tem algum erro de funcionamento:
# ARRUMAR CALENDARIO PARA PODER ALTERAL DEPOIS DE SELECIONAR 

# Botar restrição para número de contato

# Organizar cógido para ficar mais legivel

# Por algum motivo o programa só ta rodando uma vez 



windowcad.mainloop()


# Fazer versão onde ficaria tudo em uma mesma janela no formato mobile
# Não usar destroy