import csv
import random

POPULACAO_INICIAL = 100
GERACOES = 50
TAXA_MUTACAO = 0.05
ELITE = 5
acoes_csv = "cotacoes_b3_202_05.csv"

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

def gerar_individuo(acoes_disponiveis):
    return [[random.choice(acoes_disponiveis) for _ in range(10)] for _ in range(12)]

def gerar_populacao(tamanho, acoes_disponiveis):
    return [gerar_individuo(acoes_disponiveis) for _ in range(tamanho)]

def selecionar_melhores(populacao, dados_cotacoes, quantidade):
    avaliacoes = [(avaliar_dna(ind, dados_cotacoes), ind) for ind in populacao]
    avaliacoes.sort(reverse=True, key=lambda x: x[0])
    melhores = [ind for _, ind in avaliacoes[:quantidade]]
    return melhores, avaliacoes[0][0]  # Retorna os melhores + valor do melhor

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

def mutar(dna, acoes_disponiveis, taxa_mutacao):
    for dia in range(len(dna)):
        for pote in range(10):
            if random.random() < taxa_mutacao:
                dna[dia][pote] = random.choice(acoes_disponiveis)

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

def algoritmo_genetico(dados_cotacoes, acoes_disponiveis):
    populacao = gerar_populacao(POPULACAO_INICIAL, acoes_disponiveis)

    for geracao in range(GERACOES):
        melhores, melhor_valor = selecionar_melhores(populacao, dados_cotacoes, ELITE)

        nova_populacao = melhores.copy()

        while len(nova_populacao) < POPULACAO_INICIAL:
            pai1, pai2 = random.sample(melhores, 2)
            filho = crossover(pai1, pai2)
            mutar(filho, acoes_disponiveis, TAXA_MUTACAO)
            nova_populacao.append(filho)

        populacao = nova_populacao
        print(f"Geração {geracao + 1} - Melhor valor: R$ {melhor_valor:.2f}")

    melhores, melhor_valor = selecionar_melhores(populacao, dados_cotacoes, 1)
    return melhores[0], melhor_valor

if __name__ == "__main__":
    dados_cotacoes, acoes_disponiveis = carregar_dados_csv(acoes_csv)
    melhor_dna, valor_final = algoritmo_genetico(dados_cotacoes, acoes_disponiveis)

    print("\nMelhor DNA encontrado:")
    for i, dia in enumerate(melhor_dna):
        print(f"Dia {i+1}: {dia}")
    print(f"\nValor final: R$ {valor_final:.2f}")