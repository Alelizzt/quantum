#!/usr/bin/python3

# coding: utf-8
# Autor: Ivan Alejandro List (20182678007)
"""QSimulator
Simulador de maquina de turing (MT) y automatas finitos deterministas (AFD) para la clase de computacion cuantica.

uso: Simulador.py -p <programa.txt> -c <cinta.txt>

"""
__author__ = 'Ivan Alejandro List (aka Alelizzt)'
__license__ = 'GPL'
__version__ = '3.0'

import os.path
import optparse
import pyfiglet
from termcolor import colored

turing = False
automata = False

cinta_turing = False
cinta_automata = False

d = {}
F = set()

mensaje = set()
mensaje={True:'Aceptado', False:'Rechazado'}

fichero = open( "resultado.txt","w" )

def banner():
    """ Banner del script

    Muestra en pantalla un banner personalizado
    """
    mensaje = pyfiglet.figlet_format("QSimulator")
    print(colored(mensaje, 'cyan'))
    print(colored('\t\tBy @Alelizzt', 'magenta'))

def check_programa(filePrograma):
    """ Chequeo de programa

    Verifica el tipo de programa que proporciona el usuario.

    Parametro:
    filePrograma -- fichero/archivo proporcionado por el usuario

    """
    programa = open(filePrograma)
    primer_linea = programa.readline().replace(' ','').replace('*','').strip()
    programa.close()

    if( len(primer_linea) == 3 ):
        print(colored('[+] El programa es Automata','green'))
        global automata
        automata = True
    elif( len(primer_linea) == 5):
        print(colored('[+] El programa es Maquina Turing','green'))
        global turing
        turing = True
#    else:
#        print( colored( '[-] No se detecta programa, revisar sintaxis','red' ) )
#        exit(0)

def check_cinta(fileCinta):
    """ Chequeo de cinta

    Verifica que tipo de cinta proporciona el usuario, para discriminar entre cinta enfocada a la maquina turing
    de la cinta dirigida al automata finito determinista.

    Parametro:
    fileCinta -- fichero/archivo proporcionado por el usuario

    """
    cinta = open(fileCinta)
    lineas = len( cinta.readlines() )
    cinta.close()

    if( lineas == 1 ):
        global cinta_turing
        cinta_turing = True
    else:
        global cinta_automata
        cinta_automata = True

def leer_mt(mt):
    """Lectura de la Maquina Turing

    Asigna los valores necesarios para la ejecucion de la maquina, segun los caracteres de la linea leida.

    Parametro:
    mt -- fichero/archivo proporcionado por el usuario

    """
    global F, d
    programa = open(mt)
    for linea in programa:
        estadop,s,s2,direccion,n=linea.split()
        d[estadop,s,'nuevo_estado'] = n
        d[estadop,s,'nuevo_simbolo'] = s2
        d[estadop,s,'direccion'] = direccion
    programa.close()

def leer_afd(afd):
    """Lectura del Automata Finito Determinista (AFD)

    Revisa la existencia de un estado final (*) en el fichero asignado

    Parametro:
    afd -- fichero/archivo proporcionado por el usuario

    """
    global F, d
    programa = open(afd)
    for linea in programa:
        estadop,s,n = linea.split()
        if( '*' in estadop ):
            estadop = estadop.strip('*')
            F.add(estadop)
        d[estadop,s]=n
    programa.close()

def maquina_turing(estadop,cabeza,arreglo,cinta,contador):
    """Definicion de la Maquina Turing
    
    Lee el simbolo actual de la cinta, asigna la funcion de transicion en arreglo con una tupla de tres elementos:
    estado pasado, simbolo actual, nuevo simbolo; Asigna el nuevo simbolo en s2, dependiendo si encuentra r o no
    afectara el valor de la cabeza.
    Se realizara la funcion recursivamente hasta que no se encuentre una regla para el estado y el simbolo que
    lee actualmente
    
    Parametros:
    estadop  -- estado Anterior/Pasado
    cabeza   -- iterador de la cinta
    d        -- funcion de transicion
    cinta    -- lectura de cinta/ linea a leer
    contador -- paso actual / bandera para romper recursividad

    Excepciones:
    KeyError -- si estadop y simbolo_actual no tienen asignado direccion ni nuevo valor

    """
    global fichero
    if( cabeza >= 100 ):
        print(colored('[-] Error','red'))
        return
	
    if( contador > 100 ):
        print(colored('Error','red'))
        return
    try:
        simbolo_actual = cinta[cabeza]    
        n = arreglo[(estadop,simbolo_actual,'nuevo_estado')]
        s2 = d[(estadop,simbolo_actual,'nuevo_simbolo')]
        direccion = arreglo[(estadop,simbolo_actual,'direccion')]
    except(KeyError):
        print(colored('[-] Ninguna regla para el estado '+estadop+' y el simbolo '+simbolo_actual ,'red'))
        fichero.write('Ninguna regla para el estado '+estadop+' y el simbolo '+simbolo_actual)
        return

    fichero.write('Estado anterior '+estadop+' ')
    fichero.write('Simbolo anterior '+simbolo_actual+' ')
    fichero.write('Nuevo estado '+n+' ')
    fichero.write('Nuevo simbolo '+s2+' ')
    fichero.write('Direccion '+direccion+' ')
    
    cinta[cabeza] = s2 
    estado = estadop

    if direccion == "r":
        cabeza += 1
    else:
        cabeza -= 1

    print(''.join(map(str, cinta)))

    fichero.write(''.join(map(str, cinta)))
    fichero.write('\n')

    maquina_turing(n,cabeza,arreglo,cinta,contador)    

def automata_finito(d,q0,f,cinta):
    """Definicion del Automata Finito Determinista (AFD).

    Lee los simbolos de la cinta actual, los envia a una tupla junto con los estados pasados
    dentro de un arreglo temporal, dicho arreglo sera el siguiente estado pasado.
    Devuelve el estado pasado al fichero resultado.txt

    Parametros:
    d     -- funcion de transicion (diccionario)
    q0    -- estado inicial (0 por defecto)
    f     -- estado final (*estado)
    cinta -- cinta actual (linea leida)

    """
    estadop = q0
    for simbolo in cinta:
        estadop = d[ (estadop,simbolo) ]
    return estadop in f


#Ejecuta la cinta en la maquina de turing
def ejecutar_mt(fichero_cinta):
    """Ejecuta la cinta en la maquina de turing.

    Lee el fichero cinta, linea por linea y las almacena en una lista,
    la salida pasa por la funcion maquina_turing.

    Parametro:
    fichero_cinta -- fichero/archivo proporcionado por el usuario
    
    """
    global fichero,d
    cintas = open(fichero_cinta)
    for cinta in cintas:
        cinta = cinta.strip()
        cinta = list(cinta)
        maquina_turing('0',0,d,cinta,0)
    fichero.close()
    cintas.close()
    print(colored('[+] Escribiendo resultado.txt de la maquina de turing','green'))

def ejecutar_afd(fichero_cinta):
    """Ejecuta la cinta en el automata finito determinista.

    Lee el fichero cinta, linea por linea y la salida pasa por la funcion autonama_finito,
    para efectos de visualizacion, se utiliza el diccionario mensaje mostrando si el automata
    acepta o no el estado.

    Parametro:
    fichero_cinta -- fichero/archivo proporcionado por el usuario
    
    """
    global fichero,d,mensaje,F
    cintas = open(fichero_cinta)
    for cinta in cintas:
        cinta = cinta.strip()
        print('El estado de la entrada ' ,cinta, 'es', mensaje[automata_finito(d,'0',F,cinta)])
        fichero.write('El estado de la entrada '+cinta+ ' es ' + mensaje[automata_finito(d,'0',F,cinta)]+'')
    fichero.close()
    cintas.close()
    print(colored('[+] Escribiendo resultado.txt del automata','green'))

def main():
    
    # Menu de ayuda
    parser = optparse.OptionParser('Uso del simulador: %prog '+ '-p <programa> -c <cinta>')
    parser.add_option('-p','--programa',
            dest='filePrograma',
            type='string',
            help='Especifica el programa a simular')
    parser.add_option('-c','--cinta',
            dest='fileCinta',
            type='string',
            help='Especifica la cinta que utiliza el programa')
    (options, args) = parser.parse_args()
    filePrograma = options.filePrograma
    fileCinta = options.fileCinta
    
    # Si los ficheros estan vacios o no existen
    if (filePrograma == None) | (fileCinta == None):
        print (parser.usage)
        exit(0)
    if not os.path.isfile(filePrograma):
        print (colored('[-] El fichero "' + filePrograma + '" correspondiente al programa no existe','red'))
        exit(0)
    if not os.path.isfile(fileCinta):
        print (colored('[-] El fichero "' + fileCinta + '" correspondiente a la cinta no existe','red'))
        exit(0)


    banner()
    # Confirmando las estructuras del programa y la cinta
    print(colored('[!] Revisando el programa ...', 'yellow'))
    check_programa(filePrograma)
    print(colored('[!] Revisando la cinta ...', 'yellow'))
    check_cinta(fileCinta)

    if( turing and cinta_turing ):
        print(colored('[+] Ejecutando Maquina de turing','green'))
        leer_mt(filePrograma)
        ejecutar_mt(fileCinta)
    elif( automata and cinta_automata ):
        print(colored('[+] Ejecutanto Automata ...','green'))
        leer_afd(filePrograma)
        ejecutar_afd(fileCinta)
    else:
        print(colored('[-] El programa y la cinta no son compatibles.', 'red'))

if __name__ == '__main__':
    main()
