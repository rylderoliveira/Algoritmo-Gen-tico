import numpy as np
import random as rd
import matplotlib.pyplot as plt

# Declaração das constantes
UB = 3
LB = -2
NPOP = 10
NBITS = 8
NGEN = 12

# Função a ser minimizada
def f(x): return np.sin(x**2) * np.cos(x) + np.exp(-0.1*x) + np.exp(0.22*x)

# Cria a primeira população
def create(npop, nbits):
    pop = []
    for _ in range(npop):
        bits= []
        for _ in range(nbits):
            bit = rd.random()
            if bit >= 0.5:
                bit =1
            else:
                bit = 0
            bits.append(bit)
        pop.append(bits)
    return pop

# Transforma o array de bits em real 
def xreal(pop, ub, lb):
    x_real = []
    for bits in pop: 
        z = 0
        d = (ub - lb)/(2**len(bits)-1)
        bits.reverse()
        i = -1
        for item in bits:
            i += 1
            if item == 1:
                z += 2**i
        r = lb + z * d
        x_real.append(r)
    return x_real

# Retorna os pontos em fx e a nota de cada um dos valores
def fitness(x_real):
    fx = [f(i) for i in x_real]
    ordenada = sorted(fx, reverse=False)
    fit = [fx.index(i) for i in ordenada]
    return ordenada, fit

# Calcula a area percentual da roleta para cada individuo da população
def percentual(fx):
    total = sum(fx) 
    percentuais = []
    for elemento in fx:
        percentuais.append(elemento/total)
    return percentuais

# Aplica o metodo de seleção por roleta
def roullete(valor_percentual):
    soma_cumulativa = np.cumsum(valor_percentual)
    selecionados = []
    for i in range(len(valor_percentual)):
        aleatorio = rd.random()
        for index, elemento in enumerate(soma_cumulativa):
            if aleatorio <= elemento:
                selecionados.append(index)
                break
    return selecionados # Aqui ele retorna o index do vetor B selecionado

# Essa função faz o cruzamento entre os individuos e cria uma nova população
def crossover(selecionados):
    bits_selecionados = [pop[i] for i in selecionados] # Pegando o bits selecionados anteriormente
    mates = np.random.permutation(len(bits_selecionados)) # Achando os pares a serem cruzados
    crossover_site = rd.randrange(1,NBITS)
    new_pop = []
    # Esse primeiro for escolhe os pais para cruzamento
    for i in range(0,len(mates), 2):
        bit_pai_1 = bits_selecionados[mates[i]]
        bit_pai_2 = bits_selecionados[mates[i+1]]
        # Esse segundo for faz o cruzamento dos pais trocando os bits afrente do corte
        for j in range(crossover_site, len(bit_pai_1), 1):
            bit_pai_1[j], bit_pai_2[j] = bit_pai_2[j], bit_pai_1[j]
        # Aqui eu adiciono os novos individuos a nova população
        new_pop.append(bit_pai_1)
        new_pop.append(bit_pai_2)

    return new_pop

# Começo do SGA
pop = create(NPOP, NBITS)
x = np.linspace(LB,UB)
plt.plot(x,f(x),'--')
for i in range(NGEN):
    valor_x = xreal(pop,UB,LB)
    fx, fit = fitness(valor_x)
    print(fx)
    print(fit)
    percentual_fx = percentual(fx)
    print(percentual_fx)
    selecionados = roullete(percentual_fx)
    filhos = crossover(selecionados)
    pop = filhos
    plt.plot(valor_x, fx, '+')
    plt.pause(0.5)
