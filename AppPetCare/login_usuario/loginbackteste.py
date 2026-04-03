# dicionário??
# Poder trocar o nome de usuário ou senha caso optar 


# Tentando fazer sozinha:

from __future__ import annotations
import random
import string

while True:
    nome = input('Insira o nome de usuário: \n')
    if len(nome) < 3:
        print('O nome deve posssuir no mínimo 3 caracteres')
        continue
    else:
        break

while True:
    email = input('Insira seu endereço de e-mail: \n')
    if '@gmail.com' not in email:
        print('Endereço de e-mail inválido.')
        continue
    if email == '@gmail.com':
        print('Endereço de e-mail inválido.')
        continue
    if not email.endswith("@gmail.com"):
        print("Endereço de e-mail inválido.")
        continue
    else:
        arroba = email.find('@')
        usuarioemail = email[0:arroba]
        dominio = email[arroba+1:]
        break

while True:
    senha = input('Insira a senha: \n')
    if len(senha) < 3:
        print('A senha deve posssuir no mínimo 3 caracteres')
        continue
    if senha.lower() == nome.lower():
        print('Nome de usuário e senha precisam ser diferentes!')
        continue
    else:
        break

while True:
    senha_confirmaçao = input('Confirme sua senha: \n')
    if senha_confirmaçao != senha:
        print('Confirmação de senha inválida')
        continue
    else:
        break

while True:
    caracteres = string.ascii_letters + string.digits
    captcha = ''
    for i in range(6):
        captcha += random.choice(caracteres)

    confirmação = input(f'{captcha} - Insira o captcha: \n')

    if confirmação != captcha:
        print('Insira o captcha corretamente.')
        continue
    else:
        print(f'Sua conta "{nome}" foi criada com sucesso') #, end=''
        break


usuario = {
    'nome': '',
    'emailcompleto': '',
    'emailnome': '',
    'emaildominio': '', 
    'senha': ''
}

usuario.update({'nome': nome})
usuario.update({'emailcompleto': email})
usuario.update({'emailnome': usuarioemail})
usuario.update({'emaildominio': dominio})
usuario.update({'senha': senha})

for key, value in usuario.items():
    print(f'{key}: {value}')

while True:
    mudarsenha = input('Mudar senha? \n').strip().lower()

    if mudarsenha != 'sim':
        print('Login finalizado.')
        break

    senha_antiga = input('Digite a senha antiga: ')
    if senha_antiga != senha:
        print('Senha incorreta')
        continue
    
    senha2 = input('Insira a senha: \n')

    if senha2 == senha:
        print('A nova senha não pode ser igual à antiga')
        continue   

    if len(senha2) < 3:
        print('A senha deve posssuir no mínimo 3 caracteres')
        continue

    if senha2.lower() == nome.lower():
        print('Nome de usuário e senha precisam ser diferentes!')
        continue

    senha_confirmaçao = input('Confirme sua senha: \n')
    if senha_confirmaçao != senha2:
        print('Confirmação de senha inválida')
        continue

    usuario.update({'senha': senha2})
    print('Senha alterada com sucesso.')
    break

for key, value in usuario.items():
    print(f'{key}: {value}')



