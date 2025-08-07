class Jogador:
    def __init__(self, nome, score):
        self.nome = nome
        self.score = score
        self.anterior = None
        self.proximo = None

class ListaJogadores:
    def __init__(self):
        self.primeiro = None
        self.ultimo = None
        self.tamanho = 0

    def adicionar_jogador(self, nome, score):
        novo_jogador = Jogador(nome, score)

        #Lista vazia
        if self.primeiro is None:
            self.primeiro = novo_jogador
            self.ultimo = novo_jogador
            self.tamanho += 1
            return

        #Inserir em ordem decrescente (Score)
        atual = self.primeiro
        while atual is not None and atual.score >= novo_jogador.score:
            atual = atual.proximo

        if atual is None:
            #Inserir no final
            novo_jogador.anterior = self.ultimo
            self.ultimo.proximo = novo_jogador
            self.ultimo = novo_jogador
        elif atual.anterior is None:
            #Inserir no início
            novo_jogador.proximo = self.primeiro
            self.primeiro.anterior = novo_jogador
            self.primeiro = novo_jogador
        else:
            #Inserir no meio
            anterior = atual.anterior
            anterior.proximo = novo_jogador
            novo_jogador.anterior = anterior
            novo_jogador.proximo = atual
            atual.anterior = novo_jogador

        self.tamanho += 1

    def buscar_jogadores_por_nome(self, nome):
        jogadores = []
        atual = self.primeiro
        while atual is not None:
            if atual.nome.lower() == nome.lower():
                jogadores.append(atual)
            atual = atual.proximo
        return jogadores

    def obter_posicao(self, jogador):
        posicao = 1
        atual = self.primeiro
        while atual is not None:
            if atual == jogador:
                return posicao
            posicao += 1
            atual = atual.proximo
        return -1

    def exibir_informacoes_jogador(self, nome_jogador):
        jogadores = self.buscar_jogadores_por_nome(nome_jogador)

        if not jogadores:
            print(f"Jogador '{nome_jogador}' não encontrado.")
            return

        for jogador in jogadores:
            posicao = self.obter_posicao(jogador)

            print("\nInformações do Jogador:")
            print(f"Nome: {jogador.nome}")
            print(f"Score: {jogador.score}")
            print(f"Posição no Ranking: {posicao}")

            #Jogador acima
            if jogador.anterior is not None:
                print(f"Jogador Acima: {jogador.anterior.nome} (Score: {jogador.anterior.score})")
            else:
                print("Jogador Acima: Primeiro jogador")

            #Jogador abaixo
            if jogador.proximo is not None:
                print(f"Jogador Abaixo: {jogador.proximo.nome} (Score: {jogador.proximo.score})")
            else:
                print("Jogador Abaixo: Último jogador")


    def exibir_ranking_completo(self):
        print("\nRanking Completo:")
        posicao = 1
        atual = self.primeiro
        while atual is not None:
            print(f"{posicao}. {atual.nome} - {atual.score}")
            posicao += 1
            atual = atual.proximo


lista_jogadores = ListaJogadores()

# Lista de Jogadores Iniciais
lista_jogadores.adicionar_jogador("João", 1500)
lista_jogadores.adicionar_jogador("Maria", 2000)
lista_jogadores.adicionar_jogador("Pedro", 1800)
lista_jogadores.adicionar_jogador("Ana", 2200)

#Função - Exibir menu
def exibir_menu():
    print("\nMenu:")
    print("1. Adicionar jogador")
    print("2. Buscar informações de um jogador")
    print("3. Exibir ranking completo")
    print("4. Sair")

while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        nome = input("Digite o nome do jogador: ")
        try:
            score = int(input("Digite o score do jogador: "))
            lista_jogadores.adicionar_jogador(nome, score)
            print(f"Jogador {nome} adicionado com sucesso!")
        except ValueError:
            print("Score deve ser um número inteiro.")

    elif opcao == "2":
        nome = input("Digite o nome do jogador a ser buscado: ")
        lista_jogadores.exibir_informacoes_jogador(nome)

    elif opcao == "3":
        lista_jogadores.exibir_ranking_completo()

    elif opcao == "4":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Por favor, escolha uma opção de 1 a 4.")