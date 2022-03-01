from math import ceil, sqrt
import matplotlib.pyplot as plt
import numpy as np
def primo(n):
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(ceil(sqrt(n))), 2):
        if n % i == 0:
            return False
    return True

def primo1(n):# algoritmo para encontrar los numeros primos 
     if n < 3:
        return True
     for i in range(2, n):
        if n % i == 0:
            return False
     return True
 
from scipy.stats import describe # instalar con pip3
from random import shuffle
import multiprocessing
cores = multiprocessing.cpu_count()
from time import time

if __name__ == "__main__":
    desde = 10000
    hasta = 40000
    original = [x for x in range(desde, hasta + 1)]
    invertido = original[::-1]
    aleatorio = original.copy()
    replicas = 50

    org, inv, ale = [],[],[]
    for nucleos in range(1,cores-1):     
        tiempos = {"ot": [], "it": [], "at": []}
        print( CORE:",cores-nucleos,")
        with multiprocessing.Pool(processes = cores - nucleos) as pool:
            for r in range(replicas):
                t = time()
                pool.map(primo, original)
                tiempos["ot"].append(time() - t)
                t = time()
                pool.map(primo, invertido)
                tiempos["it"].append(time() - t)
                shuffle(aleatorio)
                t = time()
                pool.map(primo, aleatorio)
                tiempos["at"].append(time() - t)

        org.append(tiempos["ot"])
        inv.append(tiempos["it"])
        ale.append(tiempos["at"])
      

    pb=plt.boxplot([org[0][2:replicas-1],org[1][2:replicas-1],inv[0],inv[1],ale[0],ale[1]])
    plt.xticks([1,2,3,4,5,6],
         ['ot ','ot','it ','it','at','at'])

    plt.xlabel('')
    plt.ylabel('Distancia máxima')
    plt.tick_params(axis='x', rotation=45)
  


    colors = ['blue','red','blue','red','blue', 'red']

    for patch, color in zip(pb['boxes'], colors): 
        patch.set_color(color)
    
    plt.plot([], c='blue', label='1 nucleo')
    plt.plot([], c='red', label='2 nucleo')
   
##plt.plot([], c='pink', label='dimencion 4 ')
##plt.plot([], c='blue', label='dimencion 5')

    plt.legend()
    

    plt.show() # mandar a un archivos
