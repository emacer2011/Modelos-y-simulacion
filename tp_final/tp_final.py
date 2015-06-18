#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
from matplotlib.pylab import hist, show
from pizza import Gusto
from llamada import Llamada
from evento import Evento
from reloj import Reloj
from camioneta import Camioneta

CORRIDAS = 20
EXPERIMENTOS = 60
LLAMADAS = 100
MAX_DISTANCIA = 2000
MAX_CAMIONETAS = 4
PROB_CAMBIO = 0.3


def agregar_evento(eventos, evento):
    eventos.append(evento)
    eventos.sort(key=lambda e: e.tiempo)
    return eventos


def eliminar_evento(eventos, evento):
    eventos.remove(evento)
    eventos.sort(key=lambda e: e.tiempo)
    return eventos


def crear_gustos():
    gustos = {}
    gustos[1] = Gusto('Anchoas', 0.10)
    gustos[2] = Gusto('Muzza', 0.25)
    gustos[3] = Gusto('Napolitana', 0.22)
    gustos[4] = Gusto('Especial', 0.23)
    gustos[5] = Gusto('Calabresa', 0.15)
    return gustos


def crear_llamadas(gustos):
    llamadas = []
    reloj = 0
    for i in np.random.poisson(60/20, LLAMADAS):
        reloj += i
        llamada = Llamada(reloj, get_gusto(gustos))
        llamadas.append(llamada)
    return llamadas


def crear_camionetas():
    camionetas = []
    for i in range(MAX_CAMIONETAS):
        c = Camioneta()
        camionetas.append(c)
    return camionetas


def get_gusto(gustos):
    for gusto in gustos:
        if np.random.binomial(1, gusto.get_probabilidad()):
            return gusto
    return gustos[2]


def crear_evento_llamada(eventos, llamadas):
    for llamada in llamadas:
        eventos.append(Evento(llamada, llamada.get_hora(), "llamada_cliente"))
    return eventos


def distancia_entre_puntos(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2 - y1)**2)


def ordenar_camionetas(camionetas, llamado):
    x, y = llamado.get_ubicacion()
    camionetas.sort(key=lambda c: c.distancia_a_punto(x, y))
    return camionetas


def avanzar_reloj(reloj, nueva_hora):
    return max(reloj, nueva_hora)


def cambia_pedido():
    return np.random.binomial(1, PROB_CAMBIO)


def main():
    gustos = crear_gustos()
    for i in range(EXPERIMENTOS):
        for j in range(CORRIDAS):
            llamados_perdidos = []
            llamados_rechazados = []
            pizzas_descartadas = []
            llamados_atendidos = []
            camionetas = crear_camionetas()
            llamadas = crear_llamadas(gustos)
            eventos = crear_evento_llamada([], llamadas)
            reloj = Reloj()
            reloj.set_reloj(0)
            k = 0
            while len(eventos) > 0:
                reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                if eventos[k].tipo == "llamada_cliente":
                    llamado = eventos[k].objeto
                    x, y = llamado.get_ubicacion()
                    if distancia_entre_puntos(x, y, 0, 0) > MAX_DISTANCIA:
                        print "fuera de rango - pedido rechazado"
                        llamados_rechazados.append(llamado)
                        eliminar_evento(eventos, llamado)
                        break
                    else:
                        if llamado.timeout(reloj.get_reloj()):
                            eliminar_evento(eventos, llamado)
                            llamados_perdidos.append(llamado)
                            print "llamada perdida por timeout"
                            break
                        gusto = llamado.get_gusto()
                        camionetas = ordenar_camionetas(camionetas, llamado)
                        atendido = False
                        for c in camionetas:
                            if not c.get_ocupado():
                                if c.tiene_gusto(gusto):
                                    c.atender_llamado(llamado)
                                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), llamado.get_hora()))
                                    eventos = agregar_evento(eventos, Evento(llamado, reloj.get_reloj(), "atencion_pedido"))
                                    atendido = True
                                    print "atendida"
                                    break
                                else:
                                    if cambia_pedido():
                                        gustos_disponibles = c.get_gustos()
                                        gusto = gustos_disponibles[0]
                                        llamado.set_gusto(gusto)
                                        c.atender_llamado(llamado)
                                        reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), llamado.get_hora()))
                                        eventos = agregar_evento(eventos, Evento(c, reloj.get_reloj(), "atencion_pedido"))
                                        atendido = True
                                        print "cambio gusto"
                                    else:
                                        t_viaje = c.tiempo_a_punto(0, 0)
                                        eventos = agregar_evento(eventos, Evento(c, reloj.get_reloj()+t_viaje, "inicio_recarga"))
                                        print "recargando"
                        if atendido:
                            eventos = eliminar_evento(eventos, llamado)
                elif eventos[k].tipo == "atencion_pedido":
                    c = eventos[k].objeto
                    t_viaje = c.tiempo_a_punto(c.llamada.ubicacion)
                    eventos = agregar_evento(eventos, Evento(c, reloj.get_reloj()+t_viaje, "entrega_pedido"))
                    eventos = eliminar_evento(eventos, eventos[k])
                elif eventos[k].tipo == "entrega_pedido":
                    c = eventos[k].objeto
                    if c.llamada.timeout(reloj.get_reloj()):
                            eliminar_evento(eventos, c.llamada)
                            llamados_perdidos.append(c.llamada)
                            print "llamada perdida por timeout"
                            break
                    c.fin_atencion()
                    llamados_atendidos.append(c.llamada)
                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                elif eventos[k].tipo == "inicio_recarga":
                    t_carga, malas = c.cargar(c.llamada.gusto, gustos)
                    pizzas_descartadas.append(malas)
                    eventos = agregar_evento(eventos, Evento(c, reloj.get_reloj()+t_viaje+t_carga, "fin_recarga"))
                    eventos = eliminar_evento(eventos, eventos[k])
                elif eventos[k].tipo == "fin_recarga":
                    c = eventos[k].objeto
                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                    c.finalizar_carga(reloj.get_reloj())
                    eventos = eliminar_evento(eventos, eventos[k])
            print "fin corrida %d", j
        print "fin experimento %d", i

if __name__ == '__main__':
    main()
