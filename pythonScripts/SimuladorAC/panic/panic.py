#!/usr/bin/python3

import pycxsimulator
from pylab import *

n = 100 # tamano del espacio nxn
p = 0.10 # probabilidad de que los individuos aparezcan con pánico al inicio

"""
Se inicializa la repesentacion de los estados, con estados asignados aleatoriamente con probabilidad p.
se generan dos matrices, una para el paso temporal actual y la otra para el siguiente paso temporal,
asi poder evitar cualquier conflicto no deseado durante el proceso de actualización de los estados.
"""
def inicializar():
    global config, nextconfig
    config = zeros([n, n])#Retorna un array nxn de ceros (numpy)
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random() < p else 0 #Asigna 1 y 0 a partes aleatorias de la matriz, bajo probabilidad p
    nextconfig = zeros([n, n]) #Matriz auxiliar
    
"""
Utilizando la funcion de imshow() de pylab, se visualiza el contenido de la matriz
"""
def observar():
    global config, nextconfig
    cla() #necesario para la utilizacion de imshow()
    imshow(config, vmin = 0, vmax = 1, cmap = cm.binary) # cmap en imshow es para especificar el esquema de color utilizado en la trama

"""
Se utiliza la funcion de transicion para contar el numero de individuos con panico
y aplica las reglas del modelo
"""
def actualizar():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    count += config[(x + dx) % n, (y + dy) % n] #dx & dy coordenadas relativas alrededor de x & y (de -1 a +1) para hallar el valor de las celulas vecinas
            #La expresión (...) % n significa que el valor dentro del paréntesis está contenido dentro del rango [0,n - 1] por el operador de modulación (%). Se trata de una técnica de codificación útil para aplicar condiciones límite periódicas de manera muy sencilla. 
            nextconfig[x, y] = 1 if count >= 4 else 0 #Aplicando reglas
    config, nextconfig = nextconfig, config

pycxsimulator.GUI().start(func=[inicializar, observar, actualizar])
