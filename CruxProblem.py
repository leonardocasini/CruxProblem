from Numberjack import *
import numpy as np

def functionVert(matrix, rows, columns, obj):
    count = 0
    lastposition = 0
    for j in range(columns):
        for i in range(rows):
            if matrix[i][j] == obj:
                lastposition = i + 1
                y = j
                count = count + 1
    x = lastposition - count
    return (x, y,count)


def functionHor(matrix, rows, columns, obj):
    count = 0
    lastposition = 0
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == obj:
                lastposition = j + 1
                x = i
                count = count + 1
    y =  lastposition - count
    return (x, y, count)


def model_cruci_constraints(square, numV, numH, Ox1, Oy1, Ox2, Oy2,dv,dh, vg, hg):
    model = Model();
    for t in range(1,numV):
        x = Ox1[t]
        y = Oy1[t]
        model += Sum([square[x+ offset1][y] for offset1 in range(dv[t])]) == vg[t-1]

    for s in range(1,numH):
        v = Ox2[s]
        w = Oy2[s]
        model += Sum([square[v][w+offset2] for offset2 in range(dh[s])]) == hg[s-1]

    return (square, model)


def solve_Crux_model(param):
    am = param['A']
    bm = param['B']
    lv = param['LowValue']
    hv = param['HighValue']
    Rows = len(am)
    Columns = len(am[0])
    vc = param['VertConstraints']
    nvc = len(vc) + 1
    hc = param['HorizConstraints']
    nhc = len(hc) + 1

    square = Matrix(Rows, Columns, lv, hv)

    distVert = VarArray(nvc, 2, Columns)
    distHor = VarArray(nhc, 2, Rows)


    # X1,Y1 rappresenta punto partenza per def verticali mentre X2,Y2 per orizzontali
    X1 = VarArray(nvc, 1, Rows)
    Y1 = VarArray(nvc, 1, Columns)

    X2 = VarArray(nhc, 1, Columns)
    Y2 = VarArray(nhc, 1, Rows)

    # creo il vettore delle distanze
    # in pratica mi serve per contare quante caselle ci sono per ogni vincolo
    for t in range(1,nvc):
        (x,y,c) = functionVert(am, Rows, Columns,t)
        if c != 0:
            X1[t] = x
            Y1[t] = y
            distVert[t] = c
    for s in range(1,nhc):
        (x,y,c) = functionHor(bm, Rows, Columns, s)
        if c != 0:
            X2[s] = x
            Y2[s] = y
            distHor[s] = c

    Ox1 = np.array(X1)
    Oy1 = np.array(Y1)
    Ox2 = np.array(X2)
    Oy2 = np.array(Y2)
    dv  = np.array(distVert)
    dh = np.array(distHor)
    (square, model) = model_cruci_constraints(square, nvc, nhc, Ox1, Oy1, Ox2, Oy2,dv,dh,vc, hc)
    solver = model.load(param['solver'])  # Load the model into a solver


    print("DATA INSERED")
    print("Valori compresi nel dominio [" + str(lv) + "," + str(hv) + "] ")
    print("con definizioni verticali  " + str(vc))
    print("con definizioni orizzontali "+ str(hc))
    # display the result
    if solver.solve():
        print("SATISFIED")
        for indexI in range(Rows):
            for indexj in range(Columns):
                if am[indexI][indexj] == 0 and bm[indexI][indexj] == 0:
                        square[indexI][indexj] = 0
        print "I valori con zero corrispondo alle caselle nere"
        print square

    else:
        print("UNISATISFABLE")


solve_Crux_model(input({'solver': 'Mistral',
                        'LowValue': 1,
                        'HighValue': 9,
                        'VertConstraints': [13, 10, 8, 12, 14, 6, 4, 7],
                        'HorizConstraints': [9, 12, 14, 4, 11, 13, 15],
                        'A': [
                            [1, 2, 0, 4, 0, 7, 0],
                            [1, 2, 0, 4, 0, 7, 0],
                            [1, 2, 0, 0, 6, 7, 8],
                            [1, 0, 3, 5, 6, 0, 8],
                            [0, 0, 3, 5, 6, 0, 0]
                        ],
                        'B': [
                            [1, 1, 0, 2, 2, 2, 2],
                            [3, 3, 3, 3, 0, 0, 0],
                            [4, 4, 0, 0, 5, 5, 5],
                            [0, 0, 6, 6, 6, 0, 0],
                            [0, 7, 7, 7, 7, 7, 0]
                        ]
                        }))
#secondo problema
                        'r': 2,
                        's': 8,
                        'VertConstraints': [16, 18, 8, 5, 15],
                        'HorizConstraints': [8, 9 , 16 , 14, 14, 5],
                        'A': [
                            [1, 2, 0, 0, 5],
                            [1, 2, 3, 0, 5],
                            [1, 2, 3, 4, 5],
                            [1, 0, 0, 4, 5]
                        ],
                        'B': [
                            [1, 1, 0, 2, 2],
                            [3, 3, 3, 0, 0],
                            [4, 4, 4, 4, 4],
                            [5, 5, 0, 6, 6]
                        ]
#terzo problema. caso non risolvibile 
                        'r': 2,
                        's': 5,
                        'VertConstraints': [9, 11, 5, 11],
                        'HorizConstraints': [7, 11 , 7],
                        'A': [
                            [1, 2, 0, 4],
                            [1, 2, 3, 4],
                            [1, 0, 3, 4]
                        ],
                        'B': [
                            [1, 1, 0, 0],
                            [2, 2, 2, 2],
                            [0, 0, 3, 3]
                        ]
                                               
                        