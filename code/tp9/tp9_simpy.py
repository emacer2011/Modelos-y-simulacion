#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
from matplotlib.pylab import hist, show

CORRIDAS = 1
EXPERIMENTOS = 1
T_CORRIDA = 120


class Evento(object):
    """docstring for Evento"""
    def __init__(self, objeto, tiempo, tipo):
        super(Evento, self).__init__()
        self.objeto = objeto
        self.tiempo = int(tiempo)
        self.tipo = tipo

    def __str__(self):
        return "(%d){%s - %d}" % (self.tiempo, self.objeto.__class__.__name__.title(), self.objeto.id)

class Servidor(object):
    def __init__(self, func):
        self.id = id(self)
        self.tasa_atencion = func
        self.ocupado = False

    def atender(self, eventos, cliente, reloj):
        self.ocupado = True
        cliente.tiempo_atencion = reloj
        fin_atencion = reloj+self.tasa_atencion
        cliente.tiempo_salida = fin_atencion
        eventos = agregar_evento(eventos, Evento(cliente, reloj, "inicio_atencion"))
        eventos = agregar_evento(eventos, Evento(self, fin_atencion, "fin_atencion"))
        return eventos

    def terminar_atencion(self):
        self.ocupado = False


class Cliente(object):
    def __init__(self, tiempo_llegada):
        self.id = id(self)
        self.atendido = False
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atencion = 0
        self.tiempo_salida = 0

    def tiempo_espera(self):
        return self.tiempo_atencion - self.tiempo_llegada


def main():
    reloj = 0
    for i in range(EXPERIMENTOS):
        tiempos_medios = []
        for j in range(CORRIDAS):
            print "-"*20
            eventos = []
            clientes = generar_clientes(T_CORRIDA)
            eventos.extend(generar_evento_llegada(eventos, clientes))
            f = open("eventos_iniciales.txt", "w")
            for e in eventos:
                f.write(e.__str__()+'\n')
            f.close()
            serv_1 = Servidor(np.random.normal(15, 3))
            serv_2 = Servidor(np.random.exponential(12))
            servidores = [serv_1, serv_2]
            k = 0
            while (len(eventos) > 0):
                #algo
                e = eventos[k]
                if e.tipo == "llegada_cliente":
                    atendido = False
                    for s in servidores:
                        if not s.ocupado:
                            if not e.objeto.atendido:
                                print "Servidor: %s atiendo a: %s" % (s.id, e.objeto.id)
                                eventos = s.atender(eventos, e.objeto, reloj)
                                e.objeto.atendido = True
                                eventos = eliminar_evento(eventos, e)
                                k = 0
                                reloj = max(reloj, e.tiempo)
                            else:
                                k += 1
                                break
                        else:
                            k += 1
                            print "%s no me atendieron" % e
                            break
                elif e.tipo == "inicio_atencion":
                    print e.objeto.id
                    tiempos_medios.append(e.objeto.tiempo_espera())
                    reloj = max(reloj, e.tiempo)
                elif e.tipo == "fin_atencion":
                    #fin atencion
                    e.objeto.terminar_atencion()
                    k = 0
                    reloj = max(reloj, e.tiempo)

    print tiempos_medios
    media = np.average(tiempos_medios)
    std = np.std(tiempos_medios)
    print "media: ", media
    print "std: ", std

def generar_evento_llegada(eventos, clientes):
    lista = []
    for c in clientes:
        lista = agregar_evento(lista, Evento(c, c.tiempo_llegada, 'llegada_cliente'))
    return lista

def agregar_evento(eventos, evento):
    eventos.append(evento)
    eventos.sort(key=lambda e: e.tiempo)
    return eventos

def eliminar_evento(eventos, evento):
    eventos.remove(evento)
    eventos.sort(key=lambda e: e.tiempo)
    return eventos

def generar_clientes(tiempo):
    reloj = 0
    lista = []
    while( reloj <= tiempo):
        reloj += np.random.exponential(10)
        cliente = Cliente(reloj)
        lista.append(cliente)
    return lista

if __name__ == '__main__':
    main()


#data.sort(key=lambda tup: tup[1]) ordenar lista por tupla