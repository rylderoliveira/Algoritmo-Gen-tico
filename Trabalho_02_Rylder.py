import numpy as np
import random as rd
import matplotlib.pyplot as plt

# Declaração das constantes
UB = 3
LB = -2
NPOP = 10
NBITS = 8
NGEN = 12
EP = 0.1

# Funções que o usuario escolhe
h = 0
g = 0

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
    selecionados = []
    for _ in range(len(fit)):
        aleatorio = rd.random()
        for index, elemento in enumerate(soma_cumulativa): # Esse for percorre todos os itens ta soma_cumulativa, que esta em forma crescente
            if aleatorio <= elemento: # Como a lista esta na forma crescente, se aleatorio <= o elemento, ele obrigatoriamente caiu na sua região na roleta
                selecionados.append(index)
                break
    return selecionados # Aqui ele retorna o index do vetor B selecionado

def nota(pop):
    pass

# Aplica o metodo de seleção por torneio
def torneio(pop):
    temp_pop = pop.copy()
    temp_pop = rd.shuffle(temp_pop)
    fx_pop, _ = fitness(pop)
    fx_temp, _ = fitness(temp_pop)
    new_pop = []
    for i in range(len(pop)):
        if fx_pop[i] <= fx_temp[i]: 
            new_pop.append(pop[i])
        else:
            new_pop.append(temp_pop[i])
    return new_pop


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

# Encontra o melhor local
def findBest(pop):
    x = xreal(pop,UB,LB)
    fx, _ = fitness(x)
    fx_best = min(fx)
    index = fx.index(fx_best)
    x_best = x[index]
    return x_best, fx_best

# Faz o elitismo
def elite(pop, best_old):
    x = xreal(pop,UB,LB)
    fx, _ = fitness(x)
    best = min(fx)
    index = fx.index(best)
    bit_best = pop[index]
    if best_old < best:
        sub = rd.randint(0,len(fx)-1)
        pop[sub] = bit_best # Coloca o melhor individuo em algum lugar aleatorio da população
    else:
        best_old = best
    return pop

# Começo do SGA
pop = create(NPOP, NBITS)
plt.ion()
x = np.linspace(LB,UB)
for i in range(NGEN):
    plt.clf()
    # Encontra o melhor local na primeira geração para comparar com as proximas
    if i == 0:
        tempx = xreal(pop,UB,LB)
        fx, _ = fitness(tempx)
        best_old = min(fx)
    # Faz o elitismo
    else:
        elite(pop, best_old)
    valor_x = xreal(pop,UB,LB)
    fx, fit = fitness(valor_x)
    plt.plot(x,f(x), '--')
    plt.plot(valor_x, fx, '+')
    selecionados = roullete(fit)
    filhos = crossover(selecionados, pop)
    pop = filhos.copy()
    plt.pause(0.5)
plt.ioff()
print(findBest(pop))