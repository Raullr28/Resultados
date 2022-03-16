import numpy as np
import random
import matplotlib.pyplot as plt
from math import sqrt


n=10000
original=3.14616# pi kurt
x=[random.uniform(-1,1) for i in range(n)]#genera lista x random entre -1 y 1
y=[random.uniform(-1,1) for i in range(n)]
#plt.scatter(x, y, color='black', s=2)
#plt.show()
xd, yd=[], []
xf, yf= [], []
for s in range(n):
    d=(sqrt((x[s]**2)+(y[s]**2)))# guarda las distancias euclidianas en d
    if d <= 1:
        xd.append(x[s])
        yd.append(y[s])
    elif d > 1:
        xf.append(x[s])
        yf.append(y[s])
#plt.scatter(xd,yd, color='black', s=2)
#plt.show()
#plt.scatter(xf,yf, color='black', s=2)
#plt.show() 
proporcion_d= len(xd)/n
proporcion_f= len(xf)/n
pi_d= 4*(proporcion_d)
print(pi_d)

def valor_pi(n):
    x=[random.uniform(-1,1) for i in range(n)]
    y=[random.uniform(-1,1) for i in range(n)]
    xd, yd=[], []
    xf, yf= [], []
    for s in range(n):
        d=(sqrt((x[s]**2)+(y[s]**2)))
        if d <= 1:
            xd.append(x[s])
            yd.append(y[s])
        elif d > 1:
            xf.append(x[s])
            yf.append(y[s])
    proporcion_d= len(xd)/n
    proporcion_f= len(xf)/n
    pi_d= 4*(len(xd)/n)
    return(pi_d)

def decimales(real, obtenido):
    contador=-2 
    real, obtenido= (str(real)), (str(obtenido))
    obtenido=obtenido[:(len(real))]
    largo=min([len(real),len(obtenido)])
    for i in range(largo):
        if real[i] == obtenido[i]:
            contador=contador+1
        else:
            break
    return(contador)

cantidades=(1000,5000,15000,30000,80000,100000,1000000)
original=3.14616
print("original",original)
repeticiones=500
dec = {"cero": [], "uno": [], "dos": [], "tres": [], "cuatro": [], "cinco": []}
ABS, CUAD = [],[]
for n in cantidades:
    print(n)
    absoluto=[]
    cuadrado=[]
    dec_corr=[]
    for i in range(repeticiones):
        estimado=valor_pi(n)
        #print("estimado",estimado)
        absoluto.append(abs(original - estimado))
        cuadrado.append(((original - estimado)**2))
        dec_corr.append(decimales(original, estimado))#regresa cuantos decimales hubo semejantes
    #print(dec_corr)
    print("cuantos 0:",((dec_corr.count(0))/repeticiones)*100)
    print("cuantos 1:",((dec_corr.count(1))/repeticiones)*100)
    print("cuantos 2:",((dec_corr.count(2))/repeticiones)*100)
    print("cuantos 3:",((dec_corr.count(3))/repeticiones)*100)
    print("cuantos 4:",((dec_corr.count(4))/repeticiones)*100)
    print("cuantos 5:",((dec_corr.count(5))/repeticiones)*100)
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
uno=plt.boxplot([ABS[0],ABS[1],ABS[2],ABS[3],ABS[4],ABS[5],ABS[6]],
            patch_artist=False ,boxprops=dict(color=a),flierprops=dict(color=a),
            meanprops=dict(color=a),capprops=dict(color=a),whiskerprops=dict(color=a))    

plt.tick_params(axis='x', rotation=20)
plt.xticks([1,2,3,4,5,6,7],
           ['1000','5000','15000','30000','80000','100000','1000000'])
plt.plot([], c=a, label='ABSOLUTO')
plt.legend(loc='best')
plt.xlabel('Cantidad de datos en circunferencia')
plt.ylabel('Absoluto de diferencia de pi entre original y estimado')
plt.show()

dos=plt.boxplot([CUAD[0],CUAD[1],CUAD[2],CUAD[3],CUAD[4],CUAD[5],CUAD[6]],
            patch_artist=False, boxprops=dict(color=b),flierprops=dict(color=b),
            meanprops=dict(color=b),capprops=dict(color=b),whiskerprops=dict(color=b))
plt.tick_params(axis='x', rotation=20)
plt.xticks([1,2,3,4,5,6,7],
           ['1000','5000','15000','30000','80000','100000','1000000'])
plt.plot([], c=b, label='CUADRADO')
plt.legend(loc='best')
plt.xlabel('Cantidad de datos en circunferencia')
plt.ylabel('Cuadrado de diferencia pi entre original y estimado')
plt.show()
##### barras  
N = 7
ind = np.arange(N) 
width = 0.2
  
xvals = [dec["cero"][0],dec["cero"][1],dec["cero"][2],dec["cero"][3],dec["cero"][4],dec["cero"][5],dec["cero"][6]]
bar1 = plt.bar(ind, xvals, width, color = 'r')
  
yvals = [dec["uno"][0],dec["uno"][1],dec["uno"][2],dec["uno"][3],dec["uno"][4],dec["uno"][5],dec["uno"][6]]
bar2 = plt.bar(ind+width, yvals, width, color='g')
  
zvals = [dec["dos"][0],dec["dos"][1],dec["dos"][2],dec["dos"][3],dec["dos"][4],dec["dos"][5],dec["dos"][6]]
bar3 = plt.bar(ind+width*2, zvals, width, color = 'b')

avals = [dec["tres"][0],dec["tres"][1],dec["tres"][2],dec["tres"][3],dec["tres"][4],dec["tres"][5],dec["tres"][6]]
bar4 = plt.bar(ind+width*3, avals, width, color = 'yellow')

bvals = [dec["cuatro"][0],dec["cuatro"][1],dec["cuatro"][2],dec["cuatro"][3],dec["cuatro"][4],dec["cuatro"][5],dec["cuatro"][6]]
bar5 = plt.bar(ind+width*4, bvals, width, color = 'purple')

cvals = [dec["cinco"][0],dec["cinco"][1],dec["cinco"][2],dec["cinco"][3],dec["cinco"][4],dec["cinco"][5],dec["cinco"][6]]
bar6 = plt.bar(ind+width*5, cvals, width, color = 'orange')
plt.xlabel("Cantidad de datos en circunferencia")
plt.ylabel('Probabilidad de similitud por decimal (%)')
plt.xticks(ind+width,['1000','5000','15000','30000','80000','100000','1000000'])
plt.legend( (bar1, bar2, bar3,bar4, bar5, bar6), ('0', '1', '2','3,','4','5' ), title='decimales correctos')
plt.show()

###### radar chart
import plotly.graph_objects as go
categories = ['1000','5000','15000','30000','80000','100000','1000000']
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=[dec["cero"][0],dec["cero"][1],dec["cero"][2],dec["cero"][3],dec["cero"][4],dec["cero"][5],dec["cero"][6]],
      theta=categories,
      fill='toself',
      name='0 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["uno"][0],dec["uno"][1],dec["uno"][2],dec["uno"][3],dec["uno"][4],dec["uno"][5],dec["uno"][6]],
      theta=categories,
      fill='toself',
      name='1 decimal'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["dos"][0],dec["dos"][1],dec["dos"][2],dec["dos"][3],dec["dos"][4],dec["dos"][5],dec["dos"][6]],
      theta=categories,
      fill='toself',
      name='2 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["tres"][0],dec["tres"][1],dec["tres"][2],dec["tres"][3],dec["tres"][4],dec["tres"][5],dec["tres"][6]],
      theta=categories,
      fill='toself',
      name='3 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["cuatro"][0],dec["cuatro"][1],dec["cuatro"][2],dec["cuatro"][3],dec["cuatro"][4],dec["cuatro"][5],dec["cuatro"][6]],
      theta=categories,
      fill='toself',
      name='4 decimales'
))
fig.add_trace(go.Scatterpolar(
      r=[dec["cinco"][0],dec["cinco"][1],dec["cinco"][2],dec["cinco"][3],dec["cinco"][4],dec["cinco"][5],dec["cinco"][6]],
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

##
##
##n=10000
##original=3.14616# pi kurt
##x=[random.uniform(-1,1) for i in range(n)]#genera lista x random entre -1 y 1
##y=[random.uniform(-1,1) for i in range(n)]
###plt.scatter(x, y, color='black', s=2)
###plt.show()
##xd, yd=[], []
##xf, yf= [], []
##for s in range(n):
##    d=(sqrt((x[s]**2)+(y[s]**2)))# guarda las distancias euclidianas en d
##    if d <= 1:
##        xd.append(x[s])
##        yd.append(y[s])
##    elif d > 1:
##        xf.append(x[s])
##        yf.append(y[s])
###plt.scatter(xd,yd, color='black', s=2)
###plt.show()
###plt.scatter(xf,yf, color='black', s=2)
###plt.show() 
##proporcion_d= len(xd)/n
##proporcion_f= len(xf)/n
##pi_d= 4*(proporcion_d)
##print(pi_d)

