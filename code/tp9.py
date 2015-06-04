#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
from matplotlib.pylab import hist, show
from tp9_utils import Servidor,\
    agregar_evento,\
    generar_clientes,\
    generar_evento_llegada,\
    eliminar_evento

CORRIDAS = 1
EXPERIMENTOS = 1
T_CORRIDA = 120


def main():
    reloj = 0
    for i in range(EXPERIMENTOS):
        tiempos_medios = []
        for j in range(CORRIDAS):
            print "-"*20
            eventos = []
            clientes = generar_clientes(T_CORRIDA)
            eventos.extend(generar_evento_llegada(eventos, clientes))
            # f = open("eventos_iniciales.txt", "w")
            # for e in eventos:
            #     f.write(e.__str__()+'\n')
            # f.close()
            serv_1 = Servidor(np.random.normal(15, 3))
            serv_2 = Servidor(np.random.exponential(12))
            servidores = [serv_1, serv_2]
            k = 0
            while (len(eventos) > 0):
                e = eventos[k]
                if e.tipo == "llegada_cliente":
                    atendido = False
                    for s in servidores:
                        if not s.ocupado:
                            #print "Servidor: %s atiendo a Cliente: %s" % (s.id, e.objeto.id)
                            eventos = s.atender(eventos, e.objeto, reloj)
                            eventos = eliminar_evento(eventos, e)
                            atendido = True
                            break
                    if atendido:
                        k = 0
                        reloj = max(reloj, e.tiempo)
                        #print "Atendido! - reloj", reloj
                    else:
                        k += 1
                        #print "%s no me atendieron" % e
                elif e.tipo == "inicio_atencion":
                    print "tiempo llegada: %d, tiempo atencion: %s" % (e.objeto.tiempo_llegada, e.objeto.tiempo_atencion)
                    tiempos_medios.append(e.objeto.tiempo_espera())
                    reloj = max(reloj, e.tiempo)
                    eventos = eliminar_evento(eventos, e)
                elif e.tipo == "fin_atencion":
                    e.objeto.terminar_atencion()
                    k = 0
                    reloj = max(reloj, e.tiempo)
                    eventos = eliminar_evento(eventos, e)
                    # f = open("eventos_finales.txt", "w")
                    # for e in eventos:
                    #     f.write(e.__str__()+'\n')
                    # f.close()

    print tiempos_medios
    media = np.average(tiempos_medios)
    std = np.std(tiempos_medios)
    print "media: %.2f" % media
    print "std: %.2f" % std

if __name__ == '__main__':
    main()


#data.sort(key=lambda tup: tup[1]) ordenar lista por tupla