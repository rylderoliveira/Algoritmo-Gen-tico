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
            # Esse if faz com que eu tenha um vetor aleatorio contendo apenas 0 e 1
            if bit >= 0.5: 
                bit =1
            else:
                bit = 0
            bits.append(bit)
        pop.append(bits)
    return pop

# Transforma o vetor de bits em real 
def xreal(pop, ub, lb):
    x_real = []
    for bits in pop: 
        z = 0
        d = (ub - lb)/(2**len(bits)-1)
        #bits.reverse()
        i = -1
        for item in bits:
            i += 1
            if item == 1:
                z += 2**i
        r = lb + z * d
        x_real.append(r)
    return x_real

# Retorna a nota de cada um dos valores
def fitness(x_real):
    fx = [f(i) for i in x_real] # Retorna os pontos de x em fx
    temp_fx = fx.copy() # Criando lista temporario para calculo das notas
    ordenada = sorted(temp_fx, reverse=True) # Ordena os valores para escolha da nota
    fit = []
    for _, valor in enumerate(fx):
        index = ordenada.index(valor)
        fit.append(index+1) # Cria um lista com as notas de fx
        ordenada[index] = None # Essa linha foi necessaria para que não houvesse notas repetidas em caso de valor de fx iguais
    return fx, fit

# Aplica o metodo de seleção por roleta
def roullete(fit):
    total = sum(fit)
    soma_cumulativa = np.cumsum(fit)/total # Calcula a area de cada valor na roleta
    print(soma_cumulativa)
    selecionados = []
    for _ in range(len(fit)):
        aleatorio = rd.random()
        for index, elemento in enumerate(soma_cumulativa):
            if aleatorio <= elemento:
                selecionados.append(index)
                break
    return selecionados # Aqui ele retorna o index do vetor B selecionado

# Essa função faz o cruzamento entre os individuos e cria uma nova população
def crossover(selecionados, pop):
    bits_selecionados = [pop[i] for i in selecionados] # Pegando o bits selecionados anteriormente
    mates = np.random.permutation(len(bits_selecionados)) # Achando os pares a serem cruzados
    new_pop = []
    # Esse primeiro for escolhe os pais para cruzamento
    for i in range(0,len(mates), 2):
        crossover_site = rd.randrange(1,NBITS)
        bit_pai_1 = bits_selecionados[mates[i]].copy()
        bit_pai_2 = bits_selecionados[mates[i+1]].copy()
        # Esse segundo for faz o cruzamento dos pais trocando os bits afrente do corte
        for j in range(crossover_site, len(bit_pai_1), 1):
            bit_pai_1[j], bit_pai_2[j] = bit_pai_2[j], bit_pai_1[j]
        # Aqui eu adiciono os novos individuos a nova população
        new_pop.append(bit_pai_1)
        new_pop.append(bit_pai_2)

    return new_pop

# Começo do SGA
pop = create(NPOP, NBITS)
plt.ion()
x = np.linspace(LB,UB)
for i in range(NGEN):
    plt.clf()
    valor_x = xreal(pop,UB,LB)
    fx, fit = fitness(valor_x)
    print(fit)
    plt.plot(x,f(x), '--')
    plt.plot(valor_x, fx, '+')
    print(fx)
    selecionados = roullete(fit)
    filhos = crossover(selecionados, pop)
    pop = filhos.copy()
    plt.pause(0.5)
plt.ioff()