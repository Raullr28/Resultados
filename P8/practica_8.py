import numpy as np
from random import randint
from random import random
from math import exp, floor, log
from numpy.random import shuffle
import matplotlib.pyplot as plt
from time import time 

densidad=[(100,1000000),(300,5000),
          (55000,1500000),(7000,35000),(30000,10000000)]
replicas=150
data=[]
for k,n in densidad:
    print("########### k,n:",k,n,"#################")
    prom_rep=[]
    antes= time()
    for rep in range(replicas):
        orig = np.random.normal(size = k)
        cumulos = orig - min(orig)
        cumulos += 1 # ahora el menor vale uno
        cumulos = cumulos / sum(cumulos) # ahora suman a uno
        cumulos *= n # ahora suman a n, pero son valores decimales
        cumulos = np.round(cumulos).astype(int) # ahora son enteros
        diferencia = n - sum(cumulos) # por cuanto le hemos fallado
        cambio = 1 if diferencia > 0 else -1

        while diferencia != 0:
            p = randint(0, k - 1)
            if cambio > 0 or (cambio < 0 and cumulos[p] > 0): # sin vaciar
                cumulos[p] += cambio
                diferencia -= cambio
        assert all(cumulos != 0)
        assert sum(cumulos) == n
 
        c = np.median(cumulos) # tamaño crítico de cúmulos
        d = np.std(cumulos) / 4 # factor arbitrario para suavizar la curva
 
        def rotura(x, c, d):
            return 1 / (1 + exp((c - x) / d))
 
        def union(x, c):
            return exp(-x / c)

        def romperse(tam, cuantos):
            if tam == 1: # no se puede romper
                return [tam] * cuantos
            res = []
            for cumulo in range(cuantos):
                if random() < rotura(tam, c, d):
                    primera = randint(1, tam - 1)
                    segunda = tam - primera
                    assert primera > 0
                    assert segunda > 0
                    assert primera + segunda == tam
                    res += [primera, segunda]
                else:
                    res.append(tam) # no rompió
            assert sum(res) == tam * cuantos
            return res
 
        def unirse(tam, cuantos):
            res = []
            for cumulo in range(cuantos):
                if random() < union(tam, c):
                    res.append(-tam) # marcamos con negativo los que quieren unirse
                else:
                    res.append(tam)
            return res
 
        duracion = 50
        digitos = floor(log(duracion, 10)) + 1
        porcen=[]
        for paso in range(duracion):
            assert sum(cumulos) == n
            assert all([c > 0 for c in cumulos]) 
            (tams, freqs) = np.unique(cumulos, return_counts = True)
            cumulos = []
            assert len(tams) == len(freqs)
            for i in range(len(tams)):
                cumulos += romperse(tams[i], freqs[i]) 
            assert sum(cumulos) == n
            assert all([c > 0 for c in cumulos]) 
            (tams, freqs) = np.unique(cumulos, return_counts = True)
            cumulos = []
            assert len(tams) == len(freqs)
            for i in range(len(tams)):
                cumulos += unirse(tams[i], freqs[i])
            cumulos = np.asarray(cumulos)
            neg = cumulos < 0
            a = len(cumulos)
            juntarse = -1 * np.extract(neg, cumulos) # sacarlos y hacerlos positivos
            cumulos = np.extract(~neg, cumulos).tolist() # los demás van en una lista
            assert a == len(juntarse) + len(cumulos)
            nt = len(juntarse)
            if nt > 1:
                shuffle(juntarse) # orden aleatorio
            j = juntarse.tolist()
            while len(j) > 1: # agregamos los pares formados
                cumulos.append(j.pop(0) + j.pop(0))
            if len(j) > 0: # impar
                cumulos.append(j.pop(0)) # el ultimo no alcanzó pareja
            assert len(j) == 0
            assert sum(cumulos) == n
            assert all([c != 0 for c in cumulos])
        ##    print(cumulos)
        ##    print("valor critico",c)
            filtrados=[ i for i in cumulos if  i >= c]
        ##    print(filtrados)
            porcen.append((len(filtrados)/len(cumulos))*100)
    ##    print(porcen)
##        print("Promedio de porcentajes:",(sum(porcen)/len(porcen)))
        prom_rep.append((sum(porcen)/len(porcen)))
    data.append(prom_rep)
    final= time()-antes
print(data)

plt.violinplot(data, positions=[1,2,3,4,5])
plt.xlabel('Variantes de la tasa k /n')
plt.ylabel('Promedios de filtrados (%)')
plt.xticks([1,2,3,4,5], ['100,1M','300,5k',
          '55k,1.5M','7k,35k','30k,10M'])
plt.show()

