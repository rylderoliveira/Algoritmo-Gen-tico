import numpy as np
import random as rd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

# Declaração das constantes
# LB ou UB tem a seguinte forma LB = [x,y]
LB = [-1,-1]
UB = [1,1]
NPOP = 60 # 60
NBITS = 36 # 36
NGEN = 40 # 40
EP = 0.001
MUT = 0.25

# Funções que o usuario escolhe
def hFunc(x, y): return 8*x**2+4*y**2-1
def gFunc(x, y): return -x, -y-0.5

# Função a ser minimizada
def f(x,y): return x*y

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

def nota(pop):
    fz, h, g = fxy(pop)
    factiveis = []
    notas = []
    
    # Verifica se e factivel
    for _ in range(len(fz)):
        if all([abs(x) < EP for x in h]) and all([x <= 0 for x in g]):
            factiveis.append(True)
        else:
            factiveis.append(False)

    # Maior fz entre os factíveis
    mfz = 0
    if any(factiveis):
        todos_fz_fac = [fz[i] for i in range(len(fz)) if factiveis[i]]
        mfz = max(todos_fz_fac)


    # Penalidades
    for i, j in enumerate(factiveis):
        # Adiciona os factiveis
        if j:
            notas.append(fz)

        # Adiciona os infactiveis ajustados 
        elif j == False and mfz != 0:
            valor = g[i]
            g1 = valor[0]
            g2 = valor[1]
            notas.append(mfz+abs(h[i])+abs(g[i[0]])+abs(g[i[1]]))

        # Adiciona apenas os infactiveis
        else:
            valor = g[i]
            g1 = valor[0]
            g2 = valor[1]
            notas.append(abs(h[i])+abs(g1)+abs(g2))
    
    return notas
    

def real(bit, ub, lb):
    x_real = []
    for bits in bit:
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

def eixosReais(pop):
    bit_x = []
    bit_y = []
    for bit in pop:
        bit_x.append(bit[:NBITS//2])
        bit_y.append(bit[NBITS//2:])

    # Convertendo os bits X e Y em numeros reais
    xreal = real(bit_x,UB[0], LB[0])
    yreal = real(bit_y,UB[1], LB[1])
    return xreal, yreal

def fxy(pop):
    # Separação dos bits X e Y para conversão para real
    xreal, yreal = eixosReais(pop)

    # Resultado em Z da função objetivo
    resultadoz = [f(xreal[i],yreal[i]) for i in range(len(xreal))]
    resultadoh = [hFunc(xreal[i], yreal[i]) for i in range(len(xreal))]
    resultadog = [gFunc(xreal[i], yreal[i]) for i in range(len(xreal))]
    
    return resultadoz, resultadoh, resultadog

# Aplica o metodo de seleção por torneio
def torneio(pop):
    temp_pop = pop.copy()
    temp_pop = shuffle(temp_pop)
    fz_pop = nota(pop)
    fz_temp = nota(temp_pop)
    new_pop = []
    for i in range(len(pop)):
        if fz_pop[i] <= fz_temp[i]: 
            new_pop.append(pop[i])
        else:
            new_pop.append(temp_pop[i])
    return new_pop


# Essa função faz o cruzamento entre os individuos e cria uma nova população
def crossover(selecionados):
    bits_selecionados = selecionados # Pegando o bits selecionados anteriormente
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
ax = np.linspace(LB[0],UB[0])
ay = np.linspace(LB[1],UB[1])
x, y = np.meshgrid(ax,ay)
z = f(x,y)
for i in range(NGEN):
    plt.clf()
    fx, fy = eixosReais(pop)
    fz,_,_ = fxy(pop)
    plt.contour(x,y,z)
    plt.plot(fx,fy, '+', color='red')
    selecionados = torneio(pop)
    filhos = crossover(selecionados)
    pop = filhos.copy()
    plt.pause(0.5)
plt.ioff()
# ax = np.linspace(LB[0],UB[0])
# ay = np.linspace(LB[1],UB[1])
# x, y = np.meshgrid(ax,ay)
# z = f(x,y)
# plt.contourf(x,y,z)
# plt.show()
# for i in range(NGEN):
    # selecionados = torneio(pop)
    # ajustados = nota(selecionados)