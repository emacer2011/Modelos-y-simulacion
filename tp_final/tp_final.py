#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import math
from pizza import Gusto
from llamada import Llamada
from evento import Evento
from reloj import *
from camioneta import Camioneta
from estadisticas import Estadisticas

CORRIDAS = 10
EXPERIMENTOS = 20
LLAMADAS = 200
MAX_DISTANCIA = 2000
MAX_CAMIONETAS = 4
PROB_CAMBIO = 0.3
posiciones_x = []
posiciones_y = []


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
    for i in range(LLAMADAS):
        hora = np.random.poisson(60/20)
        reloj += hora
        llamada = Llamada(reloj, get_gusto(gustos))
        posiciones_x.append(llamada.get_ubicacion()[0])
        posiciones_y.append(llamada.get_ubicacion()[1])
        llamadas.append(llamada)
    return llamadas


def crear_camionetas(gustos):
    camionetas = []
    producidas = []
    for i in range(MAX_CAMIONETAS):
        c = Camioneta()
        camionetas.append(c)
        producidas.extend(c.cargar(gustos))
    return camionetas, producidas


def get_gusto(gustos):
    key = 0
    prob = 0
    while not prob:
        key = np.random.randint(1,len(gustos)+1)
        prob = np.random.binomial(1, gustos[key].get_probabilidad())
    return gustos[key]


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
    total_llamados_perdidos = []
    total_llamados_rechazados = []
    total_pizzas_descartadas = []
    total_llamados_atendidos = []
    total_pizzas_producidas = []
    camionetas, producidas = crear_camionetas(gustos)
    produccion_inicial = producidas
    tiene = 0
    recarga = 0
    cambia = 0
    for i in range(EXPERIMENTOS):
        llamados_perdidos = []
        llamados_rechazados = []
        llamados_atendidos = []
        pizzas_descartadas = []
        pizzas_producidas = []
        for j in range(CORRIDAS):
            llamadas = crear_llamadas(gustos)
            eventos = crear_evento_llamada([], llamadas)
            reloj = singleton(Reloj)
            reloj.set_reloj(0)
            k = 0
            while len(eventos) > 0:            
                reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                evento_atendido = False #Flag de que atendi el evento
                nuevo_evento = None
                if eventos[k].tipo == "llamada_cliente":
                    llamado = eventos[k].objeto
                    x, y = llamado.get_ubicacion()
                    if distancia_entre_puntos(x, y, 0, 0) > MAX_DISTANCIA:
                        llamados_rechazados.append(llamado)
                        evento_atendido = True
                    else:
                        if llamado.timeout(reloj.get_reloj()):
                            llamados_perdidos.append(llamado)
                            evento_atendido = True
                        else:
                            gusto = llamado.get_gusto()
                            camionetas = ordenar_camionetas(camionetas, llamado)
                            for c in camionetas:
                                if not c.get_ocupado():
                                    evento_atendido = True
                                    c.atender_llamado(llamado)
                                    if c.tiene_gusto(gusto):
                                        reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), llamado.get_hora()))
                                        nuevo_evento = Evento(c, reloj.get_reloj(), "atencion_pedido")
                                        tiene += 1
                                        break
                                    else:
                                        if cambia_pedido():
                                            gustos_disponibles = c.get_gustos()
                                            print gustos_disponibles
                                            if len(gustos_disponibles) > 0:
                                                gusto = gustos_disponibles[0]
                                                llamado.set_gusto(gusto)
                                                reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), llamado.get_hora()))
                                                nuevo_evento = Evento(c, reloj.get_reloj(), "atencion_pedido")
                                                cambia += 1
                                                break
                                            else:
                                                t_viaje = c.tiempo_a_punto(0, 0)
                                                nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje, "inicio_recarga")
                                                recarga += 1
                                                break
                                        else:
                                            t_viaje = c.tiempo_a_punto(0, 0)
                                            nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje, "inicio_recarga")
                                            recarga += 1
                                            break
                elif eventos[k].tipo == "atencion_pedido":
                    c = eventos[k].objeto
                    x, y = c.llamada.ubicacion
                    t_viaje = c.tiempo_a_punto(x, y)
                    nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje, "entrega_pedido")
                    evento_atendido = True
                elif eventos[k].tipo == "entrega_pedido":
                    current = eventos[k]
                    c = current.objeto
                    if c.llamada.timeout(reloj.get_reloj()):
                        llamados_perdidos.append(c.llamada)
                    else:
                        llamados_atendidos.append(c.llamada)
                    c.fin_atencion(reloj.get_reloj())
                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                    evento_atendido = True

                elif eventos[k].tipo == "inicio_recarga":
                    c = eventos[k].objeto
                    t_carga, malas, producidas = c.recargar(c.llamada.gusto, gustos, reloj.get_reloj())
                    pizzas_descartadas.extend(malas)
                    pizzas_producidas.extend(producidas)
                    nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje+t_carga, "fin_recarga")
                    evento_atendido = True
                elif eventos[k].tipo == "fin_recarga":
                    c = eventos[k].objeto
                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                    c.finalizar_carga(reloj.get_reloj())
                    x, y = c.llamada.get_ubicacion()
                    t_viaje = c.tiempo_a_punto(x, y)
                    nuevo_evento = Evento(c, reloj.get_reloj() + t_viaje, "atencion_pedido")
                    evento_atendido = True

                if not nuevo_evento is None:
                    eventos = agregar_evento(eventos, nuevo_evento)

                if evento_atendido:
                    eventos = eliminar_evento(eventos, eventos[k])
                    k = 0
                else:
                    k += 1

            for c in camionetas:
                print "camioneta %d %s " % (c.id, c.get_ocupado())

        pizzas_producidas.extend(produccion_inicial)
        total_llamados_perdidos.append(len(llamados_perdidos))
        total_llamados_rechazados.append(len(llamados_rechazados))
        total_llamados_atendidos.append(len(llamados_atendidos))
        total_pizzas_descartadas.append(len(pizzas_descartadas))
        total_pizzas_producidas.append(len(pizzas_producidas))
        #total_pizzas_producidas.append(produccion_inicial)

    print total_pizzas_producidas

    e = Estadisticas()
    e.set_produccion(total_pizzas_producidas, total_pizzas_descartadas)
    e.set_llamadas(total_llamados_atendidos, total_llamados_perdidos, total_llamados_rechazados)


    print "Resultados"
    print "Tiene: %d, Recarga: %d, Cambia: %d" % (tiene, recarga, cambia)
    print "Promedio de Pizzas Producidas:  %.2f - Cantidad: %d" % e.get_pizzas_producidas()
    print "Promedio de Pizzas descartadas: %.2f - Cantidad: %d (%.2f%%)" % e.get_pizzas_descartadas()
    print "Promedio de llamados total: %.2f - Cantidad: %d" % e.get_llamados_total()
    print "Promedio de llamados atendidos: %.2f - Cantidad: %d (%.2f%%)" % e.get_llamados_atendidos()
    print "Promedio de llamados perdidos:  %.2f - Cantidad: %d (%.2f%%)" % e.get_llamados_perdidos()
    print "Promedio de llamados rechazados: %.2f - Cantidad: %d (%.2f%%)" % e.get_llamados_rechazados()
    print "\nOtras estadisticas"
    stock_restante = e.get_stock_restante()
    print "Contenido de stock en camionetas: ", stock_restante
    print "Distancia recorridas (km) - Tiempo entre recargas (hs)"
    for c in camionetas:
        print " (%d) %.2f - %.2f" % (c.id, c.distancia_rec/1000, np.sum(c.tiempo_entre_rec)/60)
    e.set_posiciones(posiciones_x, posiciones_y)   
    
    detalle = {u'Anchoas': 0, u'Muzza': 0, u'Napolitana':0, u'Especial':0, u'Calabresa':0}
    for p in pizzas_producidas:
        detalle[p.gusto.nombre] += 1
    e.mostrar_estadisticas(detalle.values())


if __name__ == '__main__':
    main()
