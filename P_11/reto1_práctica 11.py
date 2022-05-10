import numpy as np
import pandas as pd
from math import sqrt, ceil
from random import randint, random
import matplotlib.pyplot as plt
 
def poli(maxdeg, varcount, termcount):
    f = []
    for t in range(termcount):
        var = randint(0, varcount - 1)
        deg = randint(1, maxdeg)
        f.append({'var': var, 'coef': random(), 'deg': deg})
    return pd.DataFrame(f)
  
def evaluate(pol, var):
    return sum([t.coef * var[pol.at[i, 'var']]**t.deg for i, t in pol.iterrows()])
 
 
def domin_by(target, challenger):
    if np.any(challenger < target):
        return False
    return np.any(challenger > target)
 
vc = 4
md = 3
tc = 5
k = 2 # cuantas funciones objetivo
obj = [poli(md, vc, tc) for i in range(k)]
minim = np.random.rand(2) > 0.5
n = 250 # cuantas soluciones aleatorias
sol = np.random.rand(n, vc)
val = np.zeros((n, k))
for i in range(n): # evaluamos las soluciones
for j in range(k):
        val[i, j] = evaluate(obj[j], sol[i])
sign = [1 + -2 * m for m in minim]
mejor1 = np.argmax(sign[0] * val[:, 0])
mejor2 = np.argmax(sign[1] * val[:, 1])
cual = {True: 'min', False: 'max'}

dom = []
for i in range(n):
    d = [domin_by(sign * val[i], sign * val[j]) for j in range(n)]
    dom.append(sum(d)) 
frente = val[[d == 0 for d in dom], :]

x= frente[:, 0]
y= frente[:, 1]
z=list(zip(x,y))
distancias=[]
for i in range(len(z)):
    for f in range(i, len(z)):
        if i != f:
            xi, yi = z[i]
            xf, yf = z[f]
            DE = sqrt((xf-xi)**2+(yf-yi)**2)
            distancias.append((DE,z[i],z[f]))
if len(z)<= 2:
    porcentaje=2
else:
    porcentaje=ceil((len(z))/2)
while((len(z))!= porcentaje):
    menor=min(distancias)
    for n in z:
        if n == menor[1]:  
            z.remove(menor[1])
    distancias.remove(menor)
cx, cy = zip(*z)

fig = plt.figure(figsize=(8, 6), dpi=300)        
ax = plt.subplot(111)
ax.plot(val[:, 0], val[:, 1], 'o', color = 'k', fillStyle = 'none')
ax.plot(frente[:, 0], frente[:, 1], 'o', color = 'lime')
plt.scatter(cx, cy,s=100, marker='s', c='None', edgecolors='red')
plt.xlabel('Primer objetivo ({:s})'.format(cual[minim[0]])) 
plt.ylabel('Segundo objetivo ({:s})'.format(cual[minim[1]])) 
plt.title('Ejemplo bidimensional')
plt.savefig('p11p_frente.png', bbox_inches='tight')
plt.close()
