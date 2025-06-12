# 📈 Otimizador de Alocação de Ações com Algoritmo Genético

Este projeto utiliza um algoritmo genético para encontrar uma estratégia de alocação de ações que maximize a lucratividade ao longo de um determinado período. A estratégia consiste em operações de day trade, comprando em um dia e vendendo no dia seguinte.

## 🚀 Sobre o Projeto

O objetivo principal é determinar a combinação de ações que, ao serem compradas e vendidas diariamente, resulta no maior retorno financeiro. Para isso, o algoritmo simula diversas gerações de "investidores" (indivíduos), onde cada um possui uma carteira de ações (DNA). Os investidores mais bem-sucedidos (elite) são selecionados e seus "DNAs" são combinados e sofrem mutações para criar a próxima geração, em um processo inspirado na seleção natural de Darwin.

A estratégia de investimento é simples:

O capital inicial é dividido em 10 partes (potes) iguais.

Cada pote é usado para comprar uma única ação em um dia.

Todas as ações compradas são vendidas no dia seguinte.

O valor total obtido com a venda é reinvestido na próxima rodada de compras.

## ⚙️ Como Funciona

O algoritmo opera através dos seguintes passos:

Carregamento dos Dados: As cotações históricas das ações são carregadas a partir de um arquivo csv.

População Inicial: Uma população inicial de "indivíduos" é criada. Cada indivíduo representa uma estratégia de investimento para 12 pares de dias, onde para cada par, uma lista de 10 ações é definida.

Avaliação (Fitness): Cada indivíduo da população é avaliado com base no lucro que sua estratégia geraria. O valor final, partindo de um capital inicial, é a sua "nota" de aptidão.

Seleção (Elitismo): Os indivíduos com as melhores avaliações (a elite) são selecionados para formar a base da próxima geração.

Crossover e Mutação:

Crossover: Os DNAs dos indivíduos de elite são combinados aleatoriamente para criar novos "filhos", herdando características de ambos os pais.

Mutação: Para garantir a diversidade genética, uma pequena parte do DNA dos filhos é alterada aleatoriamente, introduzindo novas ações na estratégia.

Nova Geração: A nova população, composta pela elite e pelos filhos gerados, substitui a antiga.

Repetição: O processo se repete por um número definido de gerações, aprimorando as estratégias a cada ciclo.

Ao final, o algoritmo apresenta o melhor "DNA" encontrado, que corresponde à sequência de alocação de ações que gerou o maior lucro.
