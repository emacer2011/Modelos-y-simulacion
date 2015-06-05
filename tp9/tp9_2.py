#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
from matplotlib.pylab import hist, show
from tp9_utils_2 import Servidor,\
    agregar_evento,\
    generar_cliente,\
    eliminar_evento

CORRIDAS = 100
EXPERIMENTOS = 60
T_CORRIDA = 15


def mostrar(lista):
    print "mostrando lista, largo: ", len(lista)
    for item in lista:
        print item

def get_clientes_en_cola(eventos):
    return len(filter(lambda e: es_cliente(e.objeto), eventos))

def es_cliente(objeto):
    return "Cliente" == objeto.__class__.__name__.title()

def main():
    tams_cola = []
    f = open("log.txt", "w")
    for i in range(EXPERIMENTOS):
        tiempos_medios = []
        for j in range(CORRIDAS):
            eventos = []
            serv_1 = Servidor(np.random.normal(15, 3))
            serv_2 = Servidor(np.random.exponential(12))
            servidores = [serv_1, serv_2]
            k = 0
            reloj = 0.0
            while (reloj <= T_CORRIDA):
                cliente = generar_cliente(reloj)
                eventos = cliente.generar_evento_llegada(eventos)
                e = eventos[k]
                if e.tipo == "llegada_cliente":
                    atendido = False
                    for s in servidores:
                        if not s.ocupado:
                            if reloj < e.objeto.tiempo_llegada:
                                eventos = s.atender(eventos, e.objeto, e.objeto.tiempo_llegada)
                            else:
                                eventos = s.atender(eventos, e.objeto, reloj)
                            eventos = eliminar_evento(eventos, e)
                            atendido = True
                            break
                    if atendido:
                        k = 0
                        reloj = max(reloj, e.tiempo)
                        clientes_en_cola = get_clientes_en_cola(eventos)
                        f.write("(E: %d,C: %d) Reloj %.5f | Clientes en cola: %d\n" % (i, j, reloj, clientes_en_cola))
                        tams_cola.append(clientes_en_cola)
                    else:
                        k += 1
                elif e.tipo == "inicio_atencion":
                    #print "tiempo llegada: %.5f, tiempo atencion: %s" % (e.objeto.tiempo_llegada, e.objeto.tiempo_atencion)
                    tiempos_medios.append(e.objeto.tiempo_espera())
                    reloj = max(reloj, e.tiempo)
                    eventos = eliminar_evento(eventos, e)
                elif e.tipo == "fin_atencion":
                    e.objeto.terminar_atencion()
                    k = 0
                    reloj = max(reloj, e.tiempo)
                    eventos = eliminar_evento(eventos, e)
    #print tiempos_medios
    f.close()
    media = np.average(tiempos_medios)
    std = np.std(tiempos_medios)
    inferior = np.average(tiempos_medios)-(std*1.96/math.sqrt(EXPERIMENTOS))
    superior = np.average(tiempos_medios)+(std*1.96/math.sqrt(EXPERIMENTOS))
    print "-"*20+"[Estadisticas]"+"-"*20
    print "Experimentos: %d" % (EXPERIMENTOS)
    print "Ejecuciones: %d" % (CORRIDAS)
    print "Tiempo/corrida: %d" % (T_CORRIDA)
    print "Tiempo promedio de espera en cola: %.2f" % media
    print "Desvio estandar: %.2f" % std
    print "Intervalo de confianza (95%%): %.3f < u < %.3f" % (inferior, superior)
    print "-"*20+"[Otros]"+"-"*20
    print "Maximo de clientes en cola: ", max(tams_cola)
    print "Utilizacion Servidor 1(%): NO CALCULADO"
    print "Utilizacion Servidor 2(%): NO CALCULADO"

if __name__ == '__main__':
    main()


#data.sort(key=lambda tup: tup[1]) ordenar lista por tupla