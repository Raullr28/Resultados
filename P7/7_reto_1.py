import matplotlib.pyplot as plt
from matplotlib import cm
from random import uniform, shuffle, random
from math import sqrt, fabs, exp
import numpy as np
import math as ma 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def g(x, y):
    return np.exp(-x**2)+ np.exp(-y**2)

low = -6
high = -low
step = 0.30
tmax = 1000

x = np.arange(low, high, step)
y = np.arange(low, high, step)
x, y = np.meshgrid(x, y)
z =np.exp(-x**2)+ np.exp(-y**2)

fig = plt.figure()
ax = fig.gca(projection='3d')
s = ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.01f'))
fig.colorbar(s, shrink=0.5, aspect=5)
plt.savefig("p7_3dinicial.png")
plt.show()

xi=[]
yi=[]
max1,max2,max3,max4,max5=[],[],[],[],[]
particula=5
enfriamiento=0.995
temperatura=100
for ciclo in range(particula):
    
    currx = uniform(low, high)
    curry = uniform(low, high)#posiciona particula
    print(currx,curry)
    [bestx, besty] = [currx, curry]
    for iteracion in range(tmax):#entra a hacer ciclo de la particula
        #mueve particula en x+right  y x-left
        deltax = uniform(0, step/2)#movimiento en x 
        leftx = currx - deltax  
        leftx = low if leftx < low+step else leftx #asegurar que la particula esta dentro 
        rightx = currx + deltax 
        rightx = high if rightx > high-step else rightx
        
        deltay = uniform(0, step/2)
        lefty = curry - deltay  
        lefty = low if lefty < low+step else lefty  
        righty = curry + deltay  
        righty = high if righty > high-step else righty

        lista=[(leftx, righty),(currx, righty),(rightx, righty),(leftx, curry),(rightx, curry),(leftx, lefty),(currx, lefty),(rightx, lefty)]
        v1 = g(leftx, righty)#valores evaluados en g 
        v2 = g(currx, righty)
        v3 = g(rightx, righty)
        v4 = g(leftx, curry)
        v5 = g(rightx, curry)
        v6 = g(leftx, lefty)
        v7 = g(currx, lefty)
        v8 = g(rightx, lefty)
        vecinos=[v1, v2, v3, v4, v5, v6, v7, v8]
        ########################################
        aleatorios=lista[:]
        shuffle(aleatorios)
        for vec in aleatorios:
            Xv, Yv =vec[0],vec[1]
            delta= g(Xv,Yv) - g(currx,curry)
            prob = exp(delta/temperatura)
            if delta > 0:
                currx,curry= Xv, Yv      
                break
            else:
                if random() < (prob):
                    currx,curry= Xv, Yv           
                    temperatura=(temperatura*(enfriamiento))
                    break
        if g(currx, curry) > g(bestx, besty):#Actualiza si es una mejor posicion 
            [bestx, besty] = [currx, curry]

############################# grafica
        p = np.arange(low, high, step)
        n = len(p)
        z = np.zeros((n, n), dtype=float)
        for i in range(n):
            x = p[i]
            for j in range(n):
                y = p[n - j - 1]  
                z[i, j] = g(x, y)
                
        xi.append(currx // step- low // step)
        yi.append(curry // step- low // step)
        if ciclo == 0:
            max1.append(((g(bestx,besty)),(bestx // step- low // step),(besty // step- low // step)))
        if ciclo == 1:
            max2.append(((g(bestx,besty)),(bestx // step- low // step),(besty // step- low // step)))
        if ciclo == 2:
            max3.append(((g(bestx,besty)),(bestx // step- low // step),(besty // step- low // step)))
        if ciclo == 3:
            max4.append(((g(bestx,besty)),(bestx // step- low // step),(besty // step- low // step)))
        if ciclo == 4:
            max5.append(((g(bestx,besty )),(bestx // step- low // step),(besty // step- low // step)))

for img in range(tmax):
    lista=[max1[img],max2[img],max3[img],max4[img],max5[img]]
    minimo=max(lista)
    mejorx, mejory=minimo[1],minimo[2]
    t = range(0, n, 5)
    l = ['{:.1f}'.format(low + i * step) for i in t]    
    fig, ax = plt.subplots(figsize=(-low, high), ncols=1)   
    pos = ax.imshow(z)
    plt.xticks(t, l)
    plt.yticks(t, l)  
    ax.scatter(xi[img], yi[img], marker='o', color='red', s=8)
    ax.scatter(xi[img+1000], yi[img+1000], marker='o', color='red', s=8)
    ax.scatter(xi[img+2000], yi[img+2000], marker='o', color='red', s=8)
    ax.scatter(xi[img+3000], yi[img+3000], marker='o', color='red', s=8)
    ax.scatter(xi[img+4000], yi[img+4000], marker='o', color='red', s=8)
    ax.scatter(mejorx, mejory, marker='x', color='black', s=20)
    fig.colorbar(pos, ax=ax)
    plt.title('{:d} paso'.format(img+1))
    if img in [49,249,499,749,999]:
        print("paso por aqui",img)
        fig.savefig('p7p_{:d}.png'.format(img), bbox_inches='tight')
##    plt.show()
    plt.close()
