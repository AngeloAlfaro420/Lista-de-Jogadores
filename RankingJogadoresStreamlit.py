import streamlit as st

# Classe Jogador (lista duplamente encadeada ordenada)
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

        if self.primeiro is None:
            self.primeiro = self.ultimo = novo_jogador
            self.tamanho += 1
            return

        atual = self.primeiro
        while atual is not None and atual.score >= novo_jogador.score:
            atual = atual.proximo

        if atual is None:
            novo_jogador.anterior = self.ultimo
            self.ultimo.proximo = novo_jogador
            self.ultimo = novo_jogador
        elif atual.anterior is None:
            novo_jogador.proximo = self.primeiro
            self.primeiro.anterior = novo_jogador
            self.primeiro = novo_jogador
        else:
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

    def obter_ranking(self):
        ranking = []
        posicao = 1
        atual = self.primeiro
        while atual is not None:
            ranking.append({
                'Posição': posicao,
                'Nome': atual.nome,
                'Score': atual.score
            })
            posicao += 1
            atual = atual.proximo
        return ranking

    def obter_info_jogador(self, nome_jogador):
        jogadores = self.buscar_jogadores_por_nome(nome_jogador)
        informacoes = []

        for jogador in jogadores:
            posicao = self.obter_posicao(jogador)
            info = {
                'Nome': jogador.nome,
                'Score': jogador.score,
                'Posição': posicao,
                'Jogador Acima': f"{jogador.anterior.nome} ({jogador.anterior.score})" if jogador.anterior else "Primeiro jogador",
                'Jogador Abaixo': f"{jogador.proximo.nome} ({jogador.proximo.score})" if jogador.proximo else "Último jogador"
            }
            informacoes.append(info)
        return informacoes

# Instância da lista de jogadores (mantida em cache entre interações)
@st.cache_resource
def obter_lista():
    lista = ListaJogadores()
    # Jogadores iniciais
    lista.adicionar_jogador("João", 1500)
    lista.adicionar_jogador("Maria", 2000)
    lista.adicionar_jogador("Pedro", 1800)
    lista.adicionar_jogador("Ana", 2200)
    return lista

lista = obter_lista()

# Interface do Streamlit
st.title("🏆 Sistema de Ranking de Jogadores")

aba = st.sidebar.radio("Escolha uma opção", ["Adicionar Jogador", "Buscar Jogador", "Exibir Ranking"])

if aba == "Adicionar Jogador":
    st.header("➕ Adicionar Jogador")
    with st.form("form_adicionar"):
        nome = st.text_input("Nome do Jogador")
        score = st.number_input("Score", min_value=0, step=10)
        enviar = st.form_submit_button("Adicionar")

    if enviar:
        if nome.strip() == "":
            st.error("Nome não pode estar vazio.")
        else:
            lista.adicionar_jogador(nome, score)
            st.success(f"Jogador '{nome}' com score {score} adicionado com sucesso!")

elif aba == "Buscar Jogador":
    st.header("🔍 Buscar Informações de um Jogador")
    nome_busca = st.text_input("Digite o nome do jogador")

    if st.button("Buscar"):
        info = lista.obter_info_jogador(nome_busca)
        if not info:
            st.warning(f"Nenhum jogador encontrado com o nome '{nome_busca}'.")
        else:
            for jogador in info:
                st.subheader(f"🎮 {jogador['Nome']}")
                st.write(f"**Score:** {jogador['Score']}")
                st.write(f"**Posição no Ranking:** {jogador['Posição']}")
                st.write(f"**Jogador Acima:** {jogador['Jogador Acima']}")
                st.write(f"**Jogador Abaixo:** {jogador['Jogador Abaixo']}")
                st.markdown("---")

elif aba == "Exibir Ranking":
    st.header("📋 Ranking Completo dos Jogadores")
    ranking = lista.obter_ranking()

    if not ranking:
        st.info("Nenhum jogador no ranking.")
    else:
        st.table(ranking)
