import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colorbar as colorbar
from matplotlib.colors import LinearSegmentedColormap

paso = 256 // 10
niveles = [i/256 for i in range(0, 256, paso)]
colores = [(niveles[i], 0, niveles[-(i + 1)]) for i in range(len(niveles))]
palette = LinearSegmentedColormap.from_list('tonos', colores, N = len(colores))
 
from math import fabs, sqrt, floor, log
eps = 0.001
def fuerza(i, shared):
    p = shared.data
    n = shared.count
    pi = p.iloc[i]
    xi = pi.x
    yi = pi.y
    ci = pi.c
    mi = pi.m
    fx, fy = 0, 0
    for j in range(n):
        pj = p.iloc[j]
        cj = pj.c
        mj = pj.m
        dire = (-1)**(1 + (ci * cj < 0))
        dire_m = (-1)**(1 + (ci * cj < 0))
        dx = xi - pj.x
        dy = yi - pj.y
        factor = dire * fabs(ci - cj) / (sqrt(dx**2 + dy**2) + eps)
        factor_masa = dire_m * ((mi * mj) / ((sqrt(dx**2 + dy**2) + eps)))
        fx = fx - dx * factor * factor_masa
        fy = fy - dy * factor * factor_masa
    
    fx = fx
    fy = fy
    return (fx, fy)
 

from os import popen, system

 
def actualiza(pos, fuerza, de):
    return max(min(pos + de * fuerza, 1), 0)
    
import multiprocessing
from itertools import repeat

if __name__ == "__main__":
    n = 15
    x = np.random.normal(size = n)
    y = np.random.normal(size = n)
    c = np.random.normal(size = n)
    m = np.random.normal(size = n)
    xmax = max(x)
    xmin = min(x)
    x = (x - xmin) / (xmax - xmin) # de 0 a 1
    ymax = max(y)
    ymin = min(y)
    y = (y - ymin) / (ymax - ymin) 
    cmax = max(c)
    cmin = min(c)
    c = 2 * (c - cmin) / (cmax - cmin) - 1 # entre -1 y 1
    masamax = max(m)
    masamin = min(m)
    m = 5 * ((m - masamin) / (masamax - masamin) + 0.1)
    m = np.round(m).astype(int)
    g = np.round(5 * c).astype(int)
    vel = [[0]]*n
    p = pd.DataFrame({'x': x, 'y': y, 'm':m, 'c': c,'vel':vel,'g':g})

    x = p['x']
    y = p['y']
    c = p['c']
    m = p['m']
    g = p['g']

    p['vel'] = [[0]]*n
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    ns.data = p 
    ns.count = n 
    tmax = 25
    digitos = floor(log(tmax, 10)) + 1
    fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
    pos = plt.scatter(p.x, p.y, c = p.g, s = (m*10), marker = 'x', cmap = palette)
    fig.colorbar(pos, ax=ax)
    plt.title('Estado inicial')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    fig.savefig('p9p_t0.png')
    plt.close()
   
    for t in range(tmax):
        with multiprocessing.Pool() as pool: # rehacer para que vea cambios en p
            f = pool.starmap(fuerza, [(i, ns) for i in range(n)])
            delta = 0.02 / max([max(fabs(fx), fabs(fy)) for (fx, fy) in f])
            p['x'] = pool.starmap(actualiza, zip(p.x, [v[0] for v in f], repeat(delta)))
            p['y'] = pool.starmap(actualiza, zip(p.y, [v[1] for v in f], repeat(delta)))
            ppa = ns.data
            n = ns.count
            for i in range(n):
              p1 = p.iloc[i]
              p2 = ppa.iloc[i]
              x1 = p1.x
              x2 = p2.x
              y1 = p1.y
              y2 = p2.y
              va = p2.vel
              v = []
              v.extend(va)
              veloc = (sqrt(((x2 - x1)**2) + ((y2 - y1)**2)))
              v.append(veloc)
              p['vel'][i] = v
            fig, ax = plt.subplots(figsize=(6, 5), ncols=1)
            pos = plt.scatter(p.x, p.y, c = p.g, s = (m*10), marker = 'x', cmap = palette)
            fig.colorbar(pos, ax=ax)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.xlim(-0.1, 1.1)
            plt.ylim(-0.1, 1.1)            
            plt.title('Paso {:d}'.format(t + 1))
            fig.savefig('p9p_t' + format(t + 1, '0{:d}'.format(digitos)) + '.png')
            plt.close()
            ns.data = p

#$$$ velocidad respecto al tiempo
    tiempo=tmax
    X=[i for i in range(1,tmax+2)]
    plt.plot(X,p['vel'][0],label=str(p['m'][0]))
    plt.plot(X,p['vel'][3],label=str(p['m'][3]))
    plt.plot(X,p['vel'][6],label=str(p['m'][6]))
    plt.plot(X,p['vel'][10],label=str(p['m'][10]))
    plt.plot(X,p['vel'][14],label=str(p['m'][14]))
    plt.xlabel('Tiempo')
    plt.ylabel('Velocidad')
    plt.legend(loc='best',title='masa')
    plt.show()
#$$$ velocidad contra masa
    plt.boxplot([p['vel'][0],p['vel'][3],p['vel'][6],p['vel'][10],p['vel'][14]])
    plt.xticks([1,2,3,4,5],[str(p['m'][0]),str(p['m'][3]),str(p['m'][6]),
                            str(p['m'][10]),str(p['m'][14])])
    plt.xlabel('Masa')
    plt.ylabel('Velocidad')
    plt.show()
#$$$ velocidad contra carga
    plt.boxplot([p['vel'][0],p['vel'][3],p['vel'][6],p['vel'][10],p['vel'][14]])
    plt.xticks([1,2,3,4,5],[str(round(p['c'][0],3)),str(round(p['c'][3],3)),str(round(p['c'][6],3)),
                            str(round(p['c'][10],3)),str(round(p['c'][14],3))])
    plt.xlabel('Carga')
    plt.ylabel('Velocidad')
    plt.show()

