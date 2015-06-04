#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
from matplotlib.pylab import hist, show

tiempo_entrega = {1: 0.25, 2: 0.75, 3: 0.95, 4: 1.0}
demanda_diaria = {0: 0.04, 1: 0.1, 2: 0.2, 3: 0.4, 4: 0.7, 5: 0.88, 6: 0.96, 7: 0.99, 8: 1.0}

COSTO_ORDEN = 50
COSTO_INV = 20/365  # calculo por unidad por dia
COSTO_FALTANTE = 25
CORRIDAS = 15
EXPERIMENTOS = 60
Q = 20
R = 15
STOCK_INI = 15


def main():
    stock = STOCK_INI
    costo_orden = []
    costo_inv = []
    costo_faltante = []
    costo_total = []
    for i in range(EXPERIMENTOS):
        costo_total.append(0)
        costo_orden.append(0)
        costo_inv.append(0)
        costo_faltante.append(0)
        pedidos = {1: 0, 2: 0, 3: 0, 4: 0}
        for j in range(CORRIDAS):
            pedidos, stock = verificar_pedidos(pedidos, stock)
            demanda = calcular_valor(demanda_diaria)
            costo_inv[i] += (stock * COSTO_INV)
            stock -= demanda
            if stock < 0:
                #demanda insatisfecha
                costo_faltante[i] += (stock * -1) * COSTO_FALTANTE
                stock = 0
            if stock < R:
                #pido
                dias = calcular_valor(tiempo_entrega)
                pedidos[dias] += Q
                costo_orden[i] += COSTO_ORDEN
            costo_total[i] = costo_orden[i]+costo_inv[i]+costo_faltante[i]
    print "costo promedio de ordenar : %.2f" % np.average(costo_orden)
    print "costo promedio de faltante : %.2f" % np.average(costo_faltante)
    print "costo promedio de inventario : %.2f" % np.average(costo_inv)
    print "costo total (15 dias): %.2f" % (np.average(costo_total))
    desv = np.std(costo_total)
    print "desvio %.2f" % desv
    inferior = np.average(costo_total)-(desv*2.56/math.sqrt(EXPERIMENTOS))
    superior = np.average(costo_total)+(desv*2.56/math.sqrt(EXPERIMENTOS))
    print "%.2f < u < %.2f" % (inferior, superior)
    hist(costo_total, 6)
    show()


def verificar_pedidos(pedidos, stock_actual):
    valores = pedidos.values()
    stock = valores.pop(0)
    valores.append(0)
    for v in range(len(valores)):
        pedidos[v+1] = valores[v]
    #print pedidos
    return pedidos, stock+stock_actual


def calcular_valor(diccionario):
    key = -1
    for k, v in diccionario.iteritems():
        val_uni = np.random.uniform(0.0, 1.0)
        if val_uni <= v:
            key = k
            break
    return key


if __name__ == '__main__':
    main()
