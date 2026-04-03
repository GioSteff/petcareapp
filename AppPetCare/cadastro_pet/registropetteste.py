# classe 

# Nome do pet, idade, raça, tipo, 
# fazer funções em relação ao peso diferindo com a raça/tipo
# fazer função em relação a idade, fazer com que a ativação dessa função seja opcional 
# fazer com que de para deletar um pet

class Pet:
    def __init__(self, nome, tipo, idade, raca, peso):
        self.nome = nome
        self.tipo = tipo
        self.idade = idade
        self.raca = raca
        self.peso = peso 

    def info(self):
        print(f'\nNome: {self.nome}')
        print(f'\nTipo: {self.tipo}')
        print(f'\nIdade: {self.idade} anos')
        print(f'\nRaça: {self.raca}')
        print(f'\nPeso: {self.peso}kg')


    @staticmethod
    def criar_pet():
            print('-----------------')
            print('Cadastre seu pet!\n')
            while True:
                nome = input('Insira o nome do pet:\n')
                if any(char.isdigit() for char in nome) or len(nome) < 3:
                    print('❌Insira um nome válido.')
                    continue
                break

            while True:
                tipo = input('Insira o tipo do pet: [gato, cachorro, pássaro, peixe, roedor]\n').strip().lower()
                if tipo not in ('gato', 'cachorro', 'pássaro', 'peixe', 'roedor'):
                    print('❌Insira um animal válido.')
                    continue
                break

            while True:
                try: 
                  idade = float(input('Insira a idade do pet:\n'))
                  if idade < 0 or idade > 30:
                      print('❌Insira uma idade válida.')
                  else:
                      break
                except ValueError:
                    print('❌Insira uma idade válida.')
                    continue

            while True:
                raca = input('Insira a raça do pet:\n')
                if any(char.isdigit() for char in raca):
                    print('❌Insira uma raça existente.')
                    continue
                break

            while True:
                try:
                  peso = float(input('Insira o peso do pet:\n'))
                  if peso < 0 or peso > 100:
                      print('❌Insira um peso válido.')
                      continue
                  else:
                      break
                except ValueError:
                    print('❌Insira um peso válido.')
                    continue


            return Pet(nome, tipo, idade, raca, peso)



    def get_tabela(self):
        return [self.nome, self.tipo, self.idade, self.raca, self.peso]
    
pets_cadastros = []

def dell_pet(pets_cadastrados):
    if not pets_cadastrados:
        print("❌ Nenhum pet cadastrado para deletar.")
        return pets_cadastrados
    
    print('\nPETS CADASTRADOS:\n')
    for i, pet in enumerate(pets_cadastrados, 1):
        print(f'{i}. {pet.nome} = {pet.tipo}')

    try:
        indice = int(input('\nInsira o índice do pet que deseja deletar o cadastro:\n'))

        if indice == 0:
            print("❌ Operação cancelada.")
            return pets_cadastrados
        
        if 1 <= indice <= len(pets_cadastrados):
            pet_removido = pets_cadastrados.pop(indice - 1)
            print(f'Pet {pet_removido.nome} deletado com sucesso.')
            return pets_cadastrados
        else:
            print('❌Número inválido.')
            return pets_cadastrados
    except ValueError:
        print('❌Insira um índice válido.')
        return pets_cadastrados


while True:
     criar_novo_pet = input('\nDeseja cadastrar um novo pet? [s/n]: ').strip().lower()
     if criar_novo_pet == 's':
       pet = Pet.criar_pet()
       pets_cadastros.append(pet)
       print(f'\nCadastro de {pet.nome} concluído com sucesso.')
       print(f'Pets cadastrados: {len(pets_cadastros)}')
       continue
     elif any(char.isdigit() for char in criar_novo_pet):
            print('Responde apenas com s/n!')
            continue
     elif criar_novo_pet == 'n':
        print('Cadastro cancelado.')
        break
     elif criar_novo_pet not in ('s', 'n'):
           print('Responde apenas com s/n!')
           continue
     else:
        continue

# inf = pet1.get_tabela()
# print(f'{nome}: {inf}')

while True:
    visualizar = input('Visualizar as informações dos pets registrados? [s/n]: ')
    if visualizar == 's':
       for i, pet in enumerate(pets_cadastros, 1):
           print(f'\n🐾Pet {i}:')
           pet.info()
           print('\n-----------------')
           
       print('\nCadastro concluído com sucesso.')
       break
    elif any(char.isdigit() for char in visualizar):
            print('Responde apenas com s/n!')
            continue
    elif visualizar == 'n':
        print('Cadastro concluído com sucesso.')
        continue
    elif visualizar not in ('s', 'n'):
           print('Responde apenas com s/n!')
           continue
    else:
        continue

while True:
    deletar_pet = input('Deseja deletar um cadastro de pet? [s/n]: ').strip().lower()
    if deletar_pet == 's':
        dell_pet(pets_cadastros)
        print('\nPETS CADASTRADOS:\n')
        for i, pet in enumerate(pets_cadastros, 1):
          print(f'{i}. {pet.nome} = {pet.tipo}')
        continue
    elif deletar_pet == 'n':
        print('Processo encerrado.')
        print('\nPETS CADASTRADOS:\n')
        for i, pet in enumerate(pets_cadastros, 1):
          print(f'{i}. {pet.nome} = {pet.tipo}')
        break
    else:
        if deletar_pet not in ('s', 'n'):
            print('❌Responda apenas com s ou n.')
            continue



# Não permitir deixar em branco, n permitir botar números no nome, tratar erros
# Poder criar vários pets com classificações diferentes, pet1, pet2, pet3...