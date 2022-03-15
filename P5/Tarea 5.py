from math import exp, pi
import numpy as np
from GeneralRandom import GeneralRandom
import multiprocessing
import math 
import re
import matplotlib.cm as cm
import matplotlib.pyplot as plt
            
def g(x):
    return (2  / (pi * (exp(x) + exp(-x))))

def decimales(real, obtenido):
    contador=-2 #omite el 0 y el punto . del conteo
    real, obtenido= (str(real)), (str(obtenido))# convierte para leer cada valor
    obtenido=obtenido[:(len(real))]# recorte para mismo tamaño
    largo=min([len(real),len(obtenido)])
    for i in range(largo):
        if real[i] == obtenido[i]:
            contador=contador+1
        else:
            break
    return(contador)

vg = np.vectorize(g)
X = np.arange(-8, 8, 0.05) # ampliar y refinar
Y = vg(X) # mayor eficiencia
correcto= 0.04883411112604931084064237
print("correcto",correcto)
desde = 2.96 
hasta = 7
pdz = (700,5000,10000,80000,300000,1000000)#,5000000)#numero de n para estimar valor
repeticiones = 100
result = {"Estimado": [], "abs": [], "cuad": [], "dec": []}
dec = {"cero": [], "uno": [], "dos": [], "tres": [], "cuatro": [], "cinco": []}
ABS, CUAD = [],[]
for pedazo in pdz:
    print("############## pedazos:",pedazo,"######################")
    absoluto=[]
    cuadrado=[]
    dec_corr=[]
    for i in range(repeticiones):
        generador = GeneralRandom(np.asarray(X), np.asarray(Y))
        V = generador.random(pedazo)[0]
        montecarlo = ((V >= desde) & (V <= hasta))
        integral = sum(montecarlo) / (pedazo)
        estimado=(pi / 2) * integral
        absoluto.append(abs(correcto - estimado))
        cuadrado.append(((correcto - estimado)**2))
        dec_corr.append(decimales(correcto, estimado))#regresa cuantos decimales hubo semejantes

    print("cuantos 0:",(dec_corr.count(0))/repeticiones)
    print("cuantos 1:",(dec_corr.count(1))/repeticiones)
    print("cuantos 2:",(dec_corr.count(2))/repeticiones)
    print("cuantos 3:",(dec_corr.count(3))/repeticiones)
    print("cuantos 4:",(dec_corr.count(4))/repeticiones)
    print("cuantos 5:",(dec_corr.count(5))/repeticiones)
    ABS.append(absoluto)
    CUAD.append(cuadrado)
    dec["cero"].append(((dec_corr.count(0))/repeticiones)*100)
    dec["uno"].append(((dec_corr.count(1))/repeticiones)*100)
    dec["dos"].append(((dec_corr.count(2))/repeticiones)*100)
    dec["tres"].append(((dec_corr.count(3))/repeticiones)*100)
    dec["cuatro"].append(((dec_corr.count(4))/repeticiones)*100)
    dec["cinco"].append(((dec_corr.count(5))/repeticiones)*100)

################ caja bigote
a="blue"
b="green"
uno=plt.boxplot([ABS[0],ABS[1],ABS[2],ABS[3],ABS[4],ABS[5]],
            patch_artist=False ,boxprops=dict(color=a),flierprops=dict(color=a),
            meanprops=dict(color=a),capprops=dict(color=a),whiskerprops=dict(color=a))    

plt.tick_params(axis='x', rotation=20)
plt.xticks([1,2,3,4,5,6],
           ['700','5000','10000','80000','300000','1000000'])
plt.plot([], c=a, label='ABSOLUTO')
plt.legend(loc='best')
plt.xlabel('Cantidad de datos pseudoaleatorios')
plt.ylabel('Absoluto de la diferencia entre original y estimado')
plt.show()

dos=plt.boxplot([CUAD[0],CUAD[1],CUAD[2],CUAD[3],CUAD[4],CUAD[5]],
            patch_artist=False, boxprops=dict(color=b),flierprops=dict(color=b),
            meanprops=dict(color=b),capprops=dict(color=b),whiskerprops=dict(color=b))
plt.tick_params(axis='x', rotation=20)
plt.xticks([1,2,3,4,5,6],
           ['700','5000','10000','80000','300000','1000000'])
plt.plot([], c=b, label='CUADRADO')
plt.legend(loc='best')
plt.xlabel('Cantidad de datos pseudoaleatorios')
plt.ylabel('Cuadrado de la diferencia entre original y estimado')
plt.show()
##### barras  
N = 6
ind = np.arange(N) 
width = 0.2
  
xvals = [dec["cero"][0],dec["cero"][1],dec["cero"][2],dec["cero"][3],dec["cero"][4],dec["cero"][5]]
bar1 = plt.bar(ind, xvals, width, color = 'r')
  
yvals = [dec["uno"][0],dec["uno"][1],dec["uno"][2],dec["uno"][3],dec["uno"][4],dec["uno"][5]]
bar2 = plt.bar(ind+width, yvals, width, color='g')
  
zvals = [dec["dos"][0],dec["dos"][1],dec["dos"][2],dec["dos"][3],dec["dos"][4],dec["dos"][5]]
bar3 = plt.bar(ind+width*2, zvals, width, color = 'b')

avals = [dec["tres"][0],dec["tres"][1],dec["tres"][2],dec["tres"][3],dec["tres"][4],dec["tres"][5]]
bar4 = plt.bar(ind+width*3, avals, width, color = 'yellow')

bvals = [dec["cuatro"][0],dec["cuatro"][1],dec["cuatro"][2],dec["cuatro"][3],dec["cuatro"][4],dec["cuatro"][5]]
bar5 = plt.bar(ind+width*4, bvals, width, color = 'purple')

cvals = [dec["cinco"][0],dec["cinco"][1],dec["cinco"][2],dec["cinco"][3],dec["cinco"][4],dec["cinco"][5]]
bar6 = plt.bar(ind+width*5, cvals, width, color = 'orange')
plt.xlabel("Cantidad de números pseudoaleatorios")
plt.ylabel('Probabilidad de similitud por decimal (%)')
plt.xticks(ind+width,['700', '5000', '10000','80000','300000','1000000'])
plt.legend( (bar1, bar2, bar3,bar4, bar5, bar6), ('0', '1', '2','3,','4','5' ), title='decimales correctos')
plt.show()

###### radar chart
import plotly.graph_objects as go
categories = ['700', '5000', '10000','80000','300000','1000000']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=[dec["cero"][0],dec["cero"][1],dec["cero"][2],dec["cero"][3],dec["cero"][4],dec["cero"][5]],
      theta=categories,
      fill='toself',
      name='0 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["uno"][0],dec["uno"][1],dec["uno"][2],dec["uno"][3],dec["uno"][4],dec["uno"][5]],
      theta=categories,
      fill='toself',
      name='1 decimal'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["dos"][0],dec["dos"][1],dec["dos"][2],dec["dos"][3],dec["dos"][4],dec["dos"][5]],
      theta=categories,
      fill='toself',
      name='2 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["tres"][0],dec["tres"][1],dec["tres"][2],dec["tres"][3],dec["tres"][4],dec["tres"][5]],
      theta=categories,
      fill='toself',
      name='3 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["cuatro"][0],dec["cuatro"][1],dec["cuatro"][2],dec["cuatro"][3],dec["cuatro"][4],dec["cuatro"][5]],
      theta=categories,
      fill='toself',
      name='4 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["cinco"][0],dec["cinco"][1],dec["cinco"][2],dec["cinco"][3],dec["cinco"][4],dec["cinco"][5]],
      theta=categories,
      fill='toself',
      name='5 decimales'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 90]
    )),
  showlegend=True
)
fig.show()
