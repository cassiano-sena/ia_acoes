import csv
import random
import time

# PROPOSTA:
# calcular a alocação de ações dia a dia que gere a maior lucratividade
# divide o valor investido em 10 potes
# cada pote é investido em uma ação
# compra um dia e vende no próximo

# IMPORTANTE:
# quanto mais gerações e maior taxa de mutação, maior probabilidade de melhores individuos (mais demorado e mais resource intensive)
# selecionar a elite e criar a próxima população a partir deles
 
POPULACAO_INICIAL = 100
GERACOES = 50
TAXA_MUTACAO = 0.05
ELITE = 5
acoes_csv = "cotacoes_b3_202_05.csv"

# dataset
def carregar_dados_csv(caminho_csv):
    dados_brutos = []
    acoes_validas = set()

    with open(caminho_csv, newline='', encoding='utf-8') as f:
        leitor = csv.reader(f, delimiter=';')
        for linha in leitor:
            if len(linha) < 3:
                continue
            data, codigo, preco = linha
            codigo = codigo.strip()
            if len(codigo) != 5:
                continue
            # troca virgula dos valoers por ponto
            try:
                preco = float(preco.replace(',', '.'))
            except ValueError:
                continue
            dados_brutos.append((data.strip(), codigo, preco))
            acoes_validas.add(codigo)

    dias_ordenados = sorted(list(set([linha[0] for linha in dados_brutos])))
    mapa_dias = {data: idx for idx, data in enumerate(dias_ordenados)}

    dados_cotacoes = [{} for _ in range(len(dias_ordenados))]
    for data, codigo, preco in dados_brutos:
        dia_idx = mapa_dias[data]
        dados_cotacoes[dia_idx][codigo] = preco

    return dados_cotacoes, list(acoes_validas)

# 1 individuo = 12 pares de dias
# cada par = 10 potes
# 1 porte = 1 acao aleatorai
def gerar_individuo(acoes_disponiveis):
    return [[random.choice(acoes_disponiveis) for _ in range(10)] for _ in range(12)]

# gera uma população de tamanho POPULACAO_INICIAL
def gerar_populacao(tamanho, acoes_disponiveis):
    return [gerar_individuo(acoes_disponiveis) for _ in range(tamanho)]

# seleciona os melhores a partir do valor da variavel ELITE
def selecionar_melhores(populacao, dados_cotacoes, quantidade):
    avaliacoes = [(avaliar_dna(ind, dados_cotacoes), ind) for ind in populacao]
    avaliacoes.sort(reverse=True, key=lambda x: x[0])
    melhores = [ind for _, ind in avaliacoes[:quantidade]]
    return melhores, avaliacoes[0][0]  # Retorna os melhores + valor do melhor

# fazer o crossover entre duas entidades, retornar entidade filho
def crossover(pai1, pai2):
    filho = []
    for dia in range(len(pai1)):
        genes = []
        for pote in range(10):
            if random.random() < 0.5:
                genes.append(pai1[dia][pote])
            else:
                genes.append(pai2[dia][pote])
        filho.append(genes)
    return filho

# fazer mutação aleatoriamente a partir de TAXA_MUTACAO
def mutar(dna, acoes_disponiveis, taxa_mutacao):
    mutacoes = 0
    for dia in range(len(dna)):
        for pote in range(10):
            if random.random() < taxa_mutacao:
                dna[dia][pote] = random.choice(acoes_disponiveis)
                mutacoes += 1
    return mutacoes

# divide o dinheiro em 10 potes iguais
# compra um dia x, vende em x + 1
# calcula o valor final
# soma os potes -> valor da proxima rodada
def avaliar_dna(dna, dados_cotacoes):
    valor_total = 1000.0
    total_dias = len(dados_cotacoes)
    max_pares = min(len(dna), (total_dias - 1) // 2)

    for par in range(max_pares):
        potes = [valor_total / 10] * 10
        dia_compra = par * 2
        dia_venda = dia_compra + 1

        for i in range(10):
            acao = dna[par][i]
            if acao not in dados_cotacoes[dia_compra] or acao not in dados_cotacoes[dia_venda]:
                continue
            preco_compra = dados_cotacoes[dia_compra][acao]
            preco_venda = dados_cotacoes[dia_venda][acao]
            quantidade = potes[i] / preco_compra
            potes[i] = quantidade * preco_venda

        valor_total = sum(potes)

    return valor_total

# main
def algoritmo_genetico(dados_cotacoes, acoes_disponiveis):
    populacao = gerar_populacao(POPULACAO_INICIAL, acoes_disponiveis)

    for geracao in range(GERACOES):
        inicio_geracao = time.time()

        # melhores, melhor_valor = selecionar_melhores(populacao, dados_cotacoes, ELITE)
        melhores, melhor_valor = selecionar_melhores(populacao, dados_cotacoes, ELITE)

        print(f"\nTop {ELITE} da Geração {geracao + 1}:")
        for idx, elite in enumerate(melhores):
            valor = avaliar_dna(elite, dados_cotacoes)
            print(f"  {idx+1}º - Valor: R$ {valor:.2f}")


        nova_populacao = melhores.copy()
        total_mutacoes = 0

        while len(nova_populacao) < POPULACAO_INICIAL:
            pai1, pai2 = random.sample(melhores, 2)
            filho = crossover(pai1, pai2)
            mutacoes = mutar(filho, acoes_disponiveis, TAXA_MUTACAO)
            total_mutacoes += mutacoes
            nova_populacao.append(filho)

        populacao = nova_populacao

        # Calcula média da população
        valores_pop = [avaliar_dna(ind, dados_cotacoes) for ind in populacao]
        media_valores = sum(valores_pop) / len(valores_pop)
        tempo = time.time() - inicio_geracao

        print(f"Geração {geracao + 1} | Melhor: R$ {melhor_valor:.2f} | Média: R$ {media_valores:.2f} | Mutações: {total_mutacoes} | {tempo:.2f}s")

    melhores, melhor_valor = selecionar_melhores(populacao, dados_cotacoes, 1)
    return melhores[0], melhor_valor

if __name__ == "__main__":
    dados_cotacoes, acoes_disponiveis = carregar_dados_csv(acoes_csv)
    melhor_dna, valor_final = algoritmo_genetico(dados_cotacoes, acoes_disponiveis)

    print("\nMelhor DNA encontrado:")
    for i, dia in enumerate(melhor_dna):
        print(f"Dia {i+1}: {dia}")
    print(f"\nValor final: R$ {valor_final:.2f}")