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

CORRIDAS = 20
EXPERIMENTOS = 60
LLAMADAS = 100


def crear_gustos():
    gustos = {}
    gustos['anchoas'] = Gusto('Anchoas', 0.10)
    gustos['muzza'] = Gusto('Muzza', 0.25)
    gustos['napolitana'] = Gusto('Napolitana', 0.22)
    gustos['especial'] = Gusto('Especial', 0.23)
    gusto['calabresa'] = Gusto('Calabresa', 0.15)
    return gustos


def crear_llamadas(gustos):
    llamadas = []
    reloj = 0
    for i in np.random.poisson(60/20, LLAMADAS):
        reloj += i
        llamada = Llamada(reloj, get_gusto(gustos))
        llamadas.append(llamada)
    return llamadas


def get_gusto(gustos):
    for gusto in gustos:
        if np.random.binomial(1, gusto.get_probabilidad()):
            return gusto
    return gustos['muzza']


def crear_evento_llamada(eventos, llamadas):
    for llamada in llamadas:
        eventos.append(Evento(llamada, llamada.get_hora(), "llamada_cliente"))
    return eventos


def main():
    gustos = crear_gustos()
    for i in range(EXPERIMENTOS):
        for j in range(CORRIDAS):
            llamadas = crear_llamadas(gustos)
            eventos = crear_evento_llamada([], llamadas)
            reloj = Reloj()
            reloj.set_reloj(0)
            k = 0
            while len(eventos) > 0:
                if eventos[k].tipo == "llamada_cliente":
                    # verificar distancia al punto central - posible rechazo
                    # ordenar camionetas por distancia al punto de llamada
                    # si esta dentro de la distancia, pedir camioneta con gusto requerido
                    # si no hay camionetas libres, encolar llamada
                    # de las camionetas libres, cual tiene el gusto requerido - enviar la mas cercana al punto de llamado - crear evento atencion_pedido
                    # si no hay ninguna preguntar si cambia de gusto por uno que tenga la camioneta mas cercana
                    # si no cambia, mando a recargar camioneta mas cercana y encolar llamada, crear evento inicio_recarga(tiempo_a_punto(punto actual y (0,0)) )
                    # verificar tiempo de espera, si supera 30 min pierde pedido
                    # Tener en cuenta recarga por vencimiento
                    pass
                elif eventos[k].tipo == "atencion_pedido":
                    # calcular tiempo_a_punto(evento.obj.llamada.ubicacion)
                    # generar evento entrega_pedido
                    # cambia estado a ocupado
                    # acumular distancia_rec en camioneta
                    pass
                elif eventos[k].tipo == "entrega_pedido":
                    # verificar tiempo de espera, si supera 30 min pierde pedido
                    # cambiar estado camioneta a libre
                    # baja el stock de la camioneta
                    pass
                elif eventos[k].tipo == "inicio_recarga":
                    # estado <- ocupado
                    # descartar pizzas vencidas
                    # cargar gusto requerido por llamada (Exponencial(10))
                    # para espacio restante recargar segun probabilidades de los otros gustos
                    # crear evento fin_recarga
                    pass
                elif eventos[k].tipo == "fin_recarga":
                    # registrar tiempo entre recargas (camioneta)
                    # cambiar estado a libre

if __name__ == '__main__':
    main()
