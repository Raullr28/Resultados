import pandas as pd 
import matplotlib.pyplot as plt
from math import floor, log, sqrt
from random import random, uniform
import numpy as np

l = 1.5
n = 50
pi = 0.05
pr = 0.02 # prob. de recuperar
v = l / 30
r = 0.1
tmax = 100
digitos = floor(log(tmax, 10)) + 1
c = {'I': 'r', 'S': 'g', 'R': 'orange'}
m = {'I': 'o', 'S': 's', 'R': '2'}
repeticiones=30
CB_picos=[]
CB_pasos=[]



for div in 1,2,0:
    print("####### velocidad 1/",div,"#########")
    pico, tmp= [], []
    for rep in range(repeticiones):
        agentes =  pd.DataFrame()
        agentes['x'] = [uniform(0, l) for i in range(n)]
        agentes['y'] = [uniform(0, l) for i in range(n)]
        agentes['dx'] = [uniform(-v, v) for i in range(n)]
        agentes['dy'] = [uniform(-v, v) for i in range(n)]
        agentes['estado'] = ['S' if random() > pi else 'I' for i in range(n)]
        epidemia = []
        for tiempo in range(tmax):
            conteos = agentes.estado.value_counts()
            infectados = conteos.get('I', 0)
            epidemia.append(infectados)
            if infectados == 0:
                break
            contagios = [False for i in range(n)]
            for i in range(n): # contagios
                a1 = agentes.iloc[i]
                if a1.estado == 'I':
                    for j in range(n):
                        a2 = agentes.iloc[j]
                        if a2.estado == 'S':
                            d = sqrt((a1.x - a2.x)**2 + (a1.y - a2.y)**2)
                            if d < r:
                                if random() < (r - d) / r:
                                    contagios[j] = True
            for i in range(n): # movimientos
                a = agentes.iloc[i]
                if contagios[i]:### genera tabla de contagiados hasta que contagia a 1
                    agentes.at[i, 'estado'] = 'I'
                elif a.estado == 'I': # ya infectado
                    if random() < pr:
                        agentes.at[i, 'estado'] = 'R'
                        
                if a.estado == 'I':
                    if div != 0:
                        x = a.x + (a.dx/div)
                        y = a.y + (a.dy/div)
                    elif div == 0:
                        x = a.x + (a.dx*div)
                        y = a.y + (a.dy*div)
                else:
                    x = a.x + a.dx
                    y = a.y + a.dy

                x = x if x < l else x - l
                y = y if y < l else y - l
                x = x if x > 0 else x + l
                y = y if y > 0 else y + l
                agentes.at[i, 'x'] = x
                agentes.at[i, 'y'] = y
        pico_max=(max(epidemia)/n)*100
        paso= (epidemia.index(max(epidemia)))
        pico.append(pico_max)#guarda el  pico maximo
        tmp.append(paso)#guarda el paso donde llego el pico
    CB_picos.append(pico)
    CB_pasos.append(tmp)

#caja bigote#
plt.boxplot([CB_picos[0],CB_picos[1],CB_picos[2]])
plt.xticks([1,2,3],
           ['normal','1/2','0'])

plt.xlabel('velocidades')
plt.ylabel('Picos de porcentajes de infectados (%)')
plt.show()

plt.boxplot([CB_pasos[0],CB_pasos[1],CB_pasos[2]])
plt.xticks([1,2,3],
           ['normal','1/2','0'])

plt.xlabel('velocidades')
plt.ylabel('Iteracion que se llego al pico')
plt.show()
print("####### ACABO #########")
