from random import randint
from math import floor, log
import pandas as pd
import numpy as np
import itertools

n=0.99
g=0.01
b=0.50

fact_des= itertools.product((n,g,b),(n,g,b),(n,g,b))
factor=[]
factor_lab=[]
for i in fact_des:
    factor.append(i)
    factor_lab.append(str(i))

CV=[]
for n, g, b in factor:
    print('##############',n,g,b,'###############')
    replicas=[]
    repeticiones=2
    for rep in range(repeticiones):
        modelos = pd.read_csv('digits_r1.txt', sep=' ', header = None)
        modelos = modelos.replace({'n': n, 'g': g, 'b': b})
        r, c = 7, 5
        dim = r * c
 
        tasa = 0.15
        tranqui = 0.99
        tope = 21
        k = tope + 1 # incl. cero
        contadores = np.zeros((k, k + 1), dtype = int)
        n = floor(log(k-1, 2)) + 1
        neuronas = np.random.rand(n, dim) # perceptrones
  
        for t in range(5000): # entrenamiento
            d = randint(0, tope)
            pixeles = 1 * (np.random.rand(dim) < modelos.iloc[d])
            correcto = '{0:05b}'.format(d)
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
            correcto = '{0:05b}'.format(d)
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
            medianprops=dict(color='lime'),widths=([0.15]*len(CV)))
plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
            17,18,19,20,21,22,23,24,25,26], factor_lab,rotation=45)
plt.xlabel('Probabilidades asignadas (n,g,b)')
plt.ylabel('Puntaje F')
plt.savefig('p10p.png', bbox_inches='tight') 
plt.show()
