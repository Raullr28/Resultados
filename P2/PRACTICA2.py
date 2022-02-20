import numpy as np 
from random import random
import matplotlib.cm as cm
import matplotlib.pyplot as plt

dur = 50
lim = 9
seq = 0
probabilidad=(0.2, 0.4, 0.6, 0.8)
dimension=(10, 15, 20)
repeticiones=(30)

def mapeo(pos,actual):
    fila = pos // dim
    columna = pos % dim
    return actual[fila, columna]

def paso(pos):
    fila = pos // dim
    columna = pos % dim
    vecindad = actual[max(0, fila - 1):min(dim, fila + 2),
                      max(0, columna - 1):min(dim, columna + 2)]
    return 1 * (np.sum(vecindad) - actual[fila, columna] == 3)

def nuevos_valores(dim,num):#hice función lo de generar inicio aleatorio por rep
    valores = [1 * (random() < p) for i in range(num)]
    actual = np.reshape(valores, (dim, dim))
    assert all([mapeo(x,actual) == valores[x]  for x in range(num)])
    return(valores, paso, actual)


if __name__ == "__main__":
    vivieron=[]
    murieron=[]
    for p in probabilidad :
        print( "Probabilidad:",p,)
        for dim in dimension:
            print(" dimensión:",dim,)
            num = dim**2
            contador_viv=0
            contador_mue=0
            for rep in range(repeticiones):
                valores, paso, actual = nuevos_valores(dim,num)#genera valores iniciales distintos por rep
                
                for iteracion in range(dur):
                    valores = [paso(x) for x in range(num)]
                    vivos = sum(valores)
                    if vivos == 0:
                        contador_mue += 1
                        break; # nadie vivo
                    if iteracion == (dur-1):
                        contador_viv += 1
                        
                    actual = np.reshape(valores, (dim, dim))
            print(contador_viv)
            print(contador_mue)
            contador_viv=((contador_viv*100)/(rep+1))
            contador_mue=((contador_mue*100)/(rep+1))
            print("contador_viv",contador_viv)
            print("contador_mue",contador_mue)
            vivieron.append(contador_viv)
            murieron.append(contador_mue)
    print(vivieron)
    print(murieron)

PB02=vivieron[0:3]
PB04=vivieron[3:6]
PB06=vivieron[6:9]
PB08=vivieron[9:12]
print("0.2",PB02)
print("0.4",PB04)
print("0.6",PB06)
print("0.8",PB08)
separacion = np.arange(3)
plt.plot(separacion,PB02,label='Nivel 0.2')
plt.scatter(separacion,PB02)
plt.plot(separacion,PB04,label='Nivel 0.4')
plt.scatter(separacion,PB04)
plt.plot(separacion,PB06,label='Nivel 0.6')
plt.scatter(separacion,PB06)
plt.plot(separacion,PB08,label='Nivel 0.8')
plt.scatter(separacion,PB08)
plt.xticks(separacion , ('10', '15', '20'))
plt.ylabel('supervivencia (%)')
plt.xlabel('Dimensiónes')
plt.title('Supervivencia de poblacion')
plt.legend()
plt.show()

