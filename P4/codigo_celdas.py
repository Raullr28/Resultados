import seaborn as sns
from math import sqrt
from PIL import Image, ImageColor
from random import randint, choice
import matplotlib.pyplot as plt
import numpy as np


def celda(pos):
    if pos in semillas:
        return semillas.index(pos)
    x, y = pos % n, pos // n
    cercano = None
    menor = n * sqrt(2)
    for i in range(k):
        (xs, ys) = semillas[i]
        dx, dy = x - xs, y - ys
        dist = sqrt(dx**2 + dy**2)
        if dist < menor:
            cercano, menor = i, dist
    return cercano
 
def inicio():
    direccion = randint(0, 3)
    if direccion == 0: # vertical abajo -> arriba
        return (0, randint(0, n - 1))
    elif direccion == 1: # izq. -> der
        return (randint(0, n - 1), 0)
    elif direccion == 2: # der. -> izq.
        return (randint(0, n - 1), n - 1)
    else:
        return (n - 1, randint(0, n - 1))

def propaga(replica):
    prob, dificil = 0.9, 0.8
    grieta = voronoi.copy()
    g = grieta.load()
    (x, y) = inicio()
    largo = 0
    negro = (0, 0, 0)
    while True:
        g[x, y] = negro
        largo += 1
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = x + dx, y + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n: # existe
               if g[vx, vy] != negro: # no tiene grieta por el momento
                   if vor[vx, vy] == vor[x, y]: # misma celda
                       interior.append(v)
                   else:
                       frontera.append(v)
        elegido = None
        if len(frontera) > 0:
            elegido = choice(frontera)
            prob = 1
        elif len(interior) > 0:
            elegido = choice(interior)
            prob *= dificil
        if elegido is not None:
            (dx, dy) = elegido
            x, y = x + dx, y + dy
        else:
            break # ya no se propaga
    if largo >= limite: # aqui decide que imprima las mayores a 80 el limite
        visual = grieta.resize((10 * n,10 * n))
        visual.save("p4pg_{:d}.png".format(replica2, grieta,contacto))
    return (largo, grieta)

def propaga2(replica2, grieta,contacto):
    prob, dificil = 0.9, 0.8
    g = grieta.load()
    (x, y) = inicio()
    largo = 0
    blanco = (255, 255, 255)
    contador=0
    while True:
        g[x, y] = blanco
        largo += 1
        frontera, interior = [], []
        for v in vecinos:
            (dx, dy) = v
            vx, vy = x + dx, y + dy
            if vx >= 0 and vx < n and vy >= 0 and vy < n: # existe
               if g[vx, vy] != blanco: # no tiene grieta por el momento
                   if vor[vx, vy] == vor[x, y]: # misma celda
                       interior.append(v)
                   else:
                       frontera.append(v)
               
               if g[vx, vy]==(0,0,0):
                   contador=1
                   g[vx, vy]=(255,0,0)# contacto color rojo donde se detuvo la propagacion
                   break
        if contador == 1:
            visual = grieta.resize((10 * n,10 * n))
            #visual.save("p8pg_{:d}.png".format(replica2))
            contacto.append([vx, vy])#guarda donde hizo contacto final 
            break
        elegido = None
        if len(frontera) > 0:
            elegido = choice(frontera)
            prob = 1
        elif len(interior) > 0:
            elegido = choice(interior)
            prob *= dificil
        if elegido is not None:
            (dx, dy) = elegido
            x, y = x + dx, y + dy
        else:
            break # ya no se propaga
    if largo >= limite: # aqui decide que imprima las mayores a 80 el limite
        visual = grieta.resize((10 * n,10 * n))
    return (largo)

sem=8, 40, 120
porcentaje=[]
for k in sem:
    print(" semillas:",k,)
    n, semillas = 80, []
    for s in range(k):
        while True:
            x, y = randint(0, n - 1), randint(0, n - 1)
            if (x, y) not in semillas:
                semillas.append((x, y))
                break
 
    celdas = [celda(i) for i in range(n * n)]
    voronoi = Image.new('RGB', (n, n))
    vor = voronoi.load()
    c = sns.color_palette("Set3", k).as_hex()
    for i in range(n * n):
        vor[i % n, i // n] = ImageColor.getrgb(c[celdas.pop(0)])
    limite, vecinos = 10, []# se modifico para que produzca mas grietas
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx != 0 or dy != 0:
                vecinos.append((dx, dy))

    rep=500
    contacto=[]#guarda cuantas veces chocaron
    for r in range(rep): # pruebas sin paralelismo
        largo, nueva_grieta =propaga(r)# para grieta 1 color negro
        if largo > limite:
            largo2 =propaga2(r,nueva_grieta,contacto)#para grieta 2 color blanca
    print(contacto)
    probabilidad= ((len(contacto))/rep)*100#convierte a porcentaje
    porcentaje.append(probabilidad)
    print("Probabilidad de contacto entre grietas es:",probabilidad, "%")
    
plt.barh((np.arange(len(porcentaje))), porcentaje)
plt.xlabel('probabilidad de contacto entre grietas (%)')
plt.ylabel('semillas')
plt.yticks([0,1,2],['8','40','120'])
plt.show()

c = ['red', 'darkorange', 'green']
plt.bar((np.arange(len(porcentaje))),porcentaje)
plt.plot((np.arange(len(porcentaje))),porcentaje, color='black')
plt.scatter((np.arange(len(porcentaje))),porcentaje,color=c)
plt.xlabel('semillas')
plt.ylabel('probabilidad de contacto entre grietas (%)')
plt.xticks([0,1,2],['8','40','120'])
plt.show()
