import numpy as np
from random import random
from random import randint
from numpy.random import shuffle
import matplotlib.pyplot as plt
from math import exp, floor, log

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

 
k = 3000
n = 1000000
d_variante= (2,4,6,8,14,'max','min')
replicas=20
grafico=[]
for suavizado in d_variante:
    prom=[]
    for iteraciones in range(replicas):
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
        if type(suavizado)!= str:
            d = np.std(cumulos) / suavizado # factor arbitrario para suavizar la curva
        else:
            if suavizado == 'max':
                d = max(cumulos)
            if suavizado == 'min':
                d = min(cumulos)### mejores resultados, mas alta cantidad filtrados
        duracion = 50
        digitos = floor(log(duracion, 10)) + 1
        filt=[]
        for paso in range(duracion):
        ##    print("cumulos iniciales:",len(cumulos))
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
            filtrados=[ i for i in cumulos if  i >= c]
            filt.append(len(filtrados))
        #    cv2.waitKey(15000)
        #print(sum(filt)/len(filt))
        prom.append((sum(filt)/len(filt)))
    grafico.append(prom)

plt.violinplot(grafico, positions=[1,2,3,4,5,6,7])
plt.xlabel('Suavizante d')
plt.ylabel('Cantidad promedio de filtrados')
plt.xticks([1,2,3,4,5,6,7], ['σ/2','σ/4','σ/6','σ/8',
                             'σ/14','max','min'])
plt.show()

spider=[np.mean(i) for i in grafico]
print(spider)
cv2.waitKey(15000)
import plotly.graph_objects as go
categories = ['σ/2','σ/4','σ/6','σ/8','σ/14','max','min']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=spider,
      theta=categories,
      fill=None,
      name='Suavizado'
))


fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[min(spider)-50, max(spider)+50]
    )),
  showlegend=True
)

fig.show()












