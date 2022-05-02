import numpy as np
import pandas as pd
from random import random, randint, sample
from numpy.random import choice
from time import time
import matplotlib.pyplot as plt
from scipy.stats import expon

def knapsack(peso_permitido, pesos, valores):
    assert len(pesos) == len(valores)
    peso_total = sum(pesos)
    valor_total = sum(valores)
    if peso_total < peso_permitido: 
        return valor_total
    else:
        V = dict()
        for w in range(peso_permitido + 1):
            V[(w, 0)] = 0
        for i in range(len(pesos)):
            peso = pesos[i]
            valor = valores[i]
            for w in range(peso_permitido + 1):
                cand = V.get((w - peso, i), -float('inf')) + valor
                V[(w, i + 1)] = max(V[(w, i)], cand)
        return max(V.values())

def ruleta(f,nf,lista):
    pt, pf = (f/len(lista)), (nf/len(lista))
    #print(pt,pf)
    results= choice([True,False], 1, p=[pt,pf])
    return(results) 

def factible(seleccion, pesos, capacidad):
    return np.inner(seleccion, pesos) <= capacidad
  
def objetivo(seleccion, valores):
    return np.inner(seleccion, valores)
 
def normalizar(data):
    menor = min(data)
    mayor = max(data)
    rango  = mayor - menor
    data = data - menor # > 0
    return data / rango # entre 0 y 1
  
def pesos1(cuantos, low, high):
    return np.round(normalizar(np.random.uniform(size = cuantos)) * (high - low) + low)
 
def valores1(pesos, low, high):
    n = len(pesos)
    valores = np.empty((n))
    for i in range(n):
        valores[i] = np.random.uniform(pesos[i], random(), 1)
    return normalizar(valores) * (high - low) + low

def pesos2(valores, low, high):
    cuantos=1/valores
    return np.round(normalizar(cuantos) * (high - low) + low)
 
def valores2(cuantos, low, high):
    valores = expon.rvs(size= cuantos)
    return normalizar(valores) * (high - low) + low

def pesos3(cuantos, low, high):
    return np.round(normalizar(np.random.normal(size = cuantos)) * (high - low) + low)
 
def valores3(pesos, low, high):
    n = len(pesos)
    valores = np.empty((n))
    magnitud=0.1
    ruido=np.random.normal(loc=5, size = n)
    ruido=ruido*magnitud
    for i in range(n):
        valores[i] = (pesos[i]**2)+ ruido[i]
    return normalizar(valores) * (high - low) + low
 
def poblacion_inicial(n, tam):
    pobl = np.zeros((tam, n))
    for i in range(tam):
        pobl[i] = (np.round(np.random.uniform(size = n))).astype(int)
    return pobl
 
def mutacion(sol, n):
    pos = randint(0, n - 1)
    mut = np.copy(sol)
    mut[pos] = 1 if sol[pos] == 0 else 0
    return mut
  
def reproduccion(x, y, n):
    pos = randint(2, n - 2)
    xy = np.concatenate([x[:pos], y[pos:]])
    yx = np.concatenate([y[:pos], x[pos:]])
    return (xy, yx)
 
n = 50
Vp=[]
Tr=[]
for regla in range(3):
    porc_dif=[]
    antes= time()
    print("############## regla:",regla,"#################")
    if regla == 0:
        pesos = pesos1(n, 15, 80)
        valores = valores1(pesos, 10, 500)
    if regla == 1:
        valores = valores2(n, 10, 500)
        pesos = pesos2(valores, 15, 80)
    if regla == 2:
        pesos = pesos3(n, 15, 80)
        valores = valores3(pesos, 10, 500)


    capacidad = int(round(sum(pesos) * 0.65))
    optimo = knapsack(capacidad, pesos, valores)
    init = 200
    replicas=4
    Tk=[]
    for k in range(replicas):
        p = poblacion_inicial(n, init)
        tam = p.shape[0]
        assert tam == init
        pm = 0.05
        rep = 50
        tmax = 50
        mejor = None
        mejores = []
        for t in range(tmax):
            d = []
            obj = [objetivo(p[i], valores) for i in range(tam)]
            fac = [factible(p[i], pesos, capacidad) for i in range(tam)]
            #print("##########",t,"###########")
            for i in range(tam): # mutarse
                Pr= ruleta(fac.count(True),fac.count(False),fac)
                if Pr==True:
                    p = np.vstack([p, mutacion(p[i], n)])
        
            for i in range(rep):  # reproducciones
                Pr= ruleta(fac.count(True),fac.count(False),fac)
                if Pr==True:
                    padres = sample(range(tam), 2)
                    hijos = reproduccion(p[padres[0]], p[padres[1]], n)
                    p = np.vstack([p, hijos[0], hijos[1]])
            tam = p.shape[0]
            d = []
            for i in range(tam):
                d.append({'idx': i, 'obj': objetivo(p[i], valores),
                          'fact': factible(p[i], pesos, capacidad)})
            d = pd.DataFrame(d).sort_values(by = ['fact', 'obj'], ascending = False)
            mantener = np.array(d.idx[:init])
            p = p[mantener, :]
            tam = p.shape[0]
            assert tam == init
            factibles = d.loc[d.fact == True,]
            mejor = max(factibles.obj)
            mejores.append(mejor)
        porc_dif.append(((optimo - mejor) / optimo)*100)
        Tk.append(time()-antes)
    Tr.append(np.mean(Tk))
    Vp.append(porc_dif)
    plt.figure(figsize=(7, 3), dpi=300)
    plt.plot(range(tmax), mejores, 'ks--', linewidth=1, markersize=5)
    plt.axhline(y = optimo, color = 'green', linewidth=3)   
    plt.xlabel('Paso')
    plt.ylabel('Mayor valor')
    plt.ylim(0.95 * min(mejores), 1.05 * optimo)
    plt.savefig('p10p.png', bbox_inches='tight') 
    plt.show()
    print(mejor, (optimo - mejor) / optimo)
print(Vp)
x= [1,2,3]
plt.bar(x, Tr)
plt.xticks([1,2,3], ['Regla 1','Regla 2','Regla 3'])
plt.ylabel('Tiempo de ejecucion (s)')
plt.show()

plt.violinplot(Vp[0], positions=[1])
plt.violinplot(Vp[1], positions=[2])
plt.violinplot(Vp[2], positions=[3])
plt.plot((),(),color='blue',label='Regla 1')
plt.plot((),(),color='orange',label='Regla 2')
plt.plot((),(),color='green',label='Regla 3')
plt.xlabel('Reglas')
plt.ylabel('Porcentaje de óptimo-resultado')
plt.legend(loc='upper right')
plt.show()
