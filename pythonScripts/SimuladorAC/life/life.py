#!/usr/bin/python3

ancho,alto=20,20
M=[[0 for i in range(ancho)] for j in range(alto)]

M[3][1]=1
M[3][2]=1
M[3][3]=1
M[2][3]=1
M[1][2]=1

for i in range(alto):
    print(M[i])
