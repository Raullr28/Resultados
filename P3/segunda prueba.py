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
    
    tiempos = {"ot": [], "it": [], "at": []}
    for x in range(1, cores-1):
     with multiprocessing.Pool(processes = x ) as pool:
         for r in range(replicas):
             t = time()
             pool.map(primo1, original)
             tiempos["ot"].append(time() - t)
             t = time()
             pool.map(primo2, invertido)
             tiempos["it"].append(time() - t)
             t = time()
             pool.map(primo1, aleatorio)
             tiempos["at"].append(time() - t)
     for tipo in tiempos:
         print('Con la cantidad de núcleos de: ', x)
         print(describe(tiempos[tipo]),tipo)
         print('')
