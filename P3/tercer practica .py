from math import ceil, sqrt
def primo1(n):# algoritmo para encontrar los numeros primos 
     if n < 3:
        return True
     for i in range(2, n):
        if n % i == 0:
            return False
     return True


def primo2(n1):
     if n1 < 4:
        return True
     if n1 % 2 == 0:
       return False
     for i in range(3, n1 - 1, 2):
        if n1 % i == 0:
            return False
     return True
 
from scipy.stats import describe # instalar con pip3
from random import shuffle
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np 
from scipy.stats import ttest_ind
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

cores = multiprocessing.cpu_count()
from time import time


if __name__ == "__main__":
    desde = 100
    hasta = 300
    original = [x for x in range(desde, hasta + 1)]#generar orden de listas 
    invertido = original[::-1]
    aleatorio = original.copy()
    replicas = 30
    shuffle(aleatorio)
    
    tiempos = {"ot1": [], "it1": [], "at1": []}
    tiempos2 = {"ot2": [], "it2": [], "at2": []}
    for x in range(1, cores-1):
        with multiprocessing.Pool(processes = x ) as pool:
            for r in range(replicas):
                t = time()
                pool.map(primo1, original)
                tiempos["ot1"].append(time() - t)
                t = time()
                pool.map(primo1, invertido)
                tiempos["it1"].append(time() - t)
                t = time()
                pool.map(primo1, aleatorio)
                tiempos["at1"].append(time() - t)
                t = time()
                pool.map(primo2, original)
                tiempos2["ot2"].append(time() - t)
                t = time()
                pool.map(primo2, invertido)
                tiempos2["it2"].append(time() - t)
                t = time()
                pool.map(primo2, aleatorio)
                tiempos2["at2"].append(time() - t)
        for tipo in tiempos:
            print('Con la cantidad de núcleos de: ', x)
            print(describe(tiempos[tipo]),tipo)
            print('')
        for tipo in tiempos2:
            print('Con la cantidad de núcleos de: ', x)
            print(describe(tiempos2[tipo]),tipo)
            print('')



    stat, p = pearsonr(tiempos["it1"],tiempos2["it2"])
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
            print('Probably independent')
    else:
        print('Probably dependent')
    
    stat, p = pearsonr(tiempos["at1"],tiempos2["ot2"])
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
            print('Probably independent')
    else:
        print('Probably dependent')
        
    stat, p = pearsonr(tiempos["ot1"],tiempos["at1"])
    print('stat=%.3f, p=%.3f' % (stat, p))
    if p > 0.05:
            print('Probably independent')
    else:
        print('Probably dependent')

        

    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos =np.arange(len(tiempos))
    performance = 3 + 10 * np.random.rand(len(tiempos))
    performance = 3 + 10 * np.random.rand(len(tiempos))
    error = np.random.rand(len(tiempos))
    ax.barh(y_pos, performance, xerr=error, align='center',
            color='green', ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tiempos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('rendimento')
    
    
    plt.show()                
    
    #stat, p = ttest_ind(tiempos, tiempos2)
    #print('stat=%.3f, p=%.3f' % (stat, p))
    #if p > 0.05:
        #print('Probably the same distribution')
    #else:
        #print('Probably different distributions')
  
