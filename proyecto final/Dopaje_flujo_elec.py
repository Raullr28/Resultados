import numpy as np
import pandas as pd
import cv2
from numpy.random import choice
import seaborn as sns
from math import sqrt, log, floor
from PIL import Image, ImageColor
from random import randint, choice
import random
import matplotlib.pyplot as plt


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
 
############################################################

n, k, semillas = 50, 30, []
for s in range(k):
    while True:
        x, y = randint(0, n - 1), randint(0, n - 1)
        if (x, y) not in semillas:
            semillas.append((x, y))
            break
dopaje = 0.8
base = round(1.0 - dopaje,2)
print(base)

col=['red','blue']
colors= np.random.choice(col, k, p=[base, dopaje]) 
celdas = [celda(i) for i in range(n * n)]
voronoi = Image.new('RGB', (n, n))
vor = voronoi.load()
digitos = floor(log(50, 10)) + 1
for i in range(n * n):
    vor[i % n, i // n] = ImageColor.getrgb(colors[celdas.pop(0)])
limite, vecinos = n, []
for dx in range(-1, 2):
    for dy in range(-1, 2):
        if dx != 0 or dy != 0:
            vecinos.append((dx, dy))
            
crystal_b=[]
crystal_d=[]
for y in range(n):
    for x in range(n):
        px= voronoi.getpixel((x,y))
        if px==(255,0,0):
            crystal_b.append(px)
        if px==(0,0,255):
            crystal_d.append(px)

arr= np.array(voronoi)# array[Y,X]= [fila,columna]
arr2= np.array(voronoi.copy())
cnt=0
for z in range(n): 
    arr2[z+cnt,z+cnt]=(0,255,0)
    X=[random.randint(0,n-1) for i in range(n)]
    Y=[random.randint(0,n-1)for i in range(n)]
    pix=list(zip(Y, X))
    cuantos=[]
    for i in pix:
        cuantos.append(list(arr[i]))
    rojos=cuantos.count([255,0,0])
    azules=cuantos.count([0,0,255])
    val=np.random.choice([0,1], 1, p=[rojos/n, azules/n]) 
    plt.imshow(arr2)
    plt.title('ciclo {:d}'.format(z + 1))
    plt.savefig('p9p_t' + format(z + 1, '0{:d}'.format(digitos)) + '.png')
    arr2[z+cnt,z+cnt]=arr[z+cnt,z+cnt]
    cnt=cnt+val
    if cnt+z >= n-1:
        break
termino = z
print(termino)
plt.imshow(arr)
plt.show()







