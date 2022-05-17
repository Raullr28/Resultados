from random import randint
import random
from math import floor, log
import pandas as pd
import numpy as np
import itertools


n=0.99
g=0.01
b=0.01


CV=[]
prob_ruido=(0.2,0.4,0.6,0.9)
for Pr in prob_ruido:
    print('##############',Pr,'###############')
    replicas=[]
    repeticiones=10
    for rep in range(repeticiones):
        modelos = pd.read_csv('digits.txt', sep=' ', header = None)
        modelos = modelos.replace({'n':n, 'g': g, 'b': b})
        r, c = 5, 3
        dim = r * c
 
        tasa = 0.15
        tranqui = 0.99
        tope = 9
        k = tope + 1 # incl. cero
        contadores = np.zeros((k, k + 1), dtype = int)
        n = floor(log(k-1, 2)) + 1
        neuronas = np.random.rand(n, dim) # perceptrones
  
        for t in range(5000): # entrenamiento
            d = randint(0, tope)
            pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d])

            cnt=0
            for pix in pixeles:
                if (random.uniform(0, 1)) > Pr:
                    pixeles.iloc[cnt]=random.randint(0, 1)
                cnt=cnt+1
                
            correcto = '{0:04b}'.format(d)
            for i in range(n):
                w = neuronas[i, :]
                deseada = int(correcto[i]) # 0 o 1
                resultado = sum(w * pixeles) >= 0
                if deseada != resultado: 
                    ajuste = tasa * (1 * deseada - 1 * resultado)
                    tasa = tranqui * tasa 
                    neuronas[i, :] = w + ajuste * pixeles
 
        for t in range(300): # prueba
            d = randint(0, tope)
            pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d])

            cnt=0
            for pix in pixeles:
                if (random.uniform(0, 1)) > Pr:
                    pixeles.iloc[cnt]=random.randint(0, 1)
                cnt=cnt+1
            
            correcto = '{0:04b}'.format(d)
            salida = ''
            for i in range(n):
                salida += '1' if sum(neuronas[i, :] * pixeles) >= 0 else '0'
            r = min(int(salida, 2), k)
            contadores[d, r] += 1
        c = pd.DataFrame(contadores)
        c.columns = [str(i) for i in range(k)] + ['NA']
        c.index = [str(i) for i in range(k)]

        diagonal=[]
        for d in range(0,k):
            num=c.iloc[d][d]
            diagonal.append(num)

        FP=[]
        for e in c.columns[0:-1]:
            suma=sum(c[e])
            diag=diagonal[int(e)]
            FP.append(suma-diag)
            
        FN=[f for f in c['NA']]

        PCS= sum(diagonal)/(sum(diagonal)+sum(FP))
        RCL=sum(diagonal)/(sum(diagonal)+sum(FN))
        F_score= 2*(PCS*RCL)/(PCS+RCL)
        replicas.append(F_score)
    CV.append(replicas)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5), dpi=300)
plt.violinplot(CV)
c='red'
plt.boxplot(CV,
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color='lime'),widths=([0.25]*len(CV)))
plt.xticks([1,2,3,4], [str(i)for i in prob_ruido])
plt.xlabel('Probabilidad de ruido sal y pimienta')
plt.ylabel('Puntaje F')
plt.savefig('p15p.png', bbox_inches='tight') 
plt.show()

