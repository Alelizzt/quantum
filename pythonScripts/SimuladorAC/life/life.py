#!/usr/bin/python3

ancho,alto=20,20
M=[[0 for i in range(ancho)] for j in range(alto)]

M[3][1]=1
M[3][2]=1
M[3][3]=1
M[2][3]=1
M[1][2]=1

'''
U|T|V
L|C|R
W|B|X
'''
def applyRules(m):
    temp = [[0 for i in range(ancho)] for j in range(alto)]
    for i in range(alto):
        for j in range(ancho):
            if i==0:#condicion de frontera periodicas
                iprev=alto-1
            else:
                iprev=i-1
            if i==alto-1:
                inext=0
            else:
                inext=i+1
            if j==0: #ahora con las columnas
                jprev=ancho-1
            else:
                jprev=j-1
            if j==ancho-1:
                jnext=0
            else:
                jnext=j+1
            C=m[i][j]
            L=m[i][jprev]
            R=m[i][jnext]
            T=m[iprev][j]
            B=m[inext][j]
            U=m[iprev][jprev]
            V=m[iprev][jnext]
            W=m[inext][jprev]
            X=m[inext][jnext]

            v=[L,R,T,B,U,V,W,X]
            S=sum(v)
            N=0
            #Aplicando la regla del juego de la vida
            if C==0 and S==3:
                N=1
            if C==1 and (S==2)|(S==3):
                N=1
            temp[i][j]=N

    return temp

def imprimir():
    for i in range(alto):
        print(M[i])


def graficar(num):
    imagen=open("img_%03d.pbm"%num,"w")
    imagen.write("P1 "+str(ancho)+" "+str(alto))
    for i in range(alto):
        for j in range(ancho):
            imagen.write(" "+str(M[i][j]))
    imagen.close()

for num in range(80):
    graficar(num)
    M=applyRules(M)
#imprimir()
