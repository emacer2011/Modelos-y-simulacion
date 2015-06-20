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

CORRIDAS = 5
EXPERIMENTOS = 5
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
    for i in range(LLAMADAS):
        hora = np.random.poisson(60/20)
        reloj += hora
        llamada = Llamada(reloj, get_gusto(gustos))
        llamadas.append(llamada)
    return llamadas


def crear_camionetas(gustos):
    camionetas = []
    producidas = []
    for i in range(MAX_CAMIONETAS):
        c = Camioneta()
        camionetas.append(c)
        producidas.extend(c.cargar(gustos))
        print "Cree %d pizzas para la camioneta %s" % (len(c.pizzas), c.id)
        #for p in c.pizzas:
        #    print p.gusto.nombre
    return camionetas, producidas


def get_gusto(gustos):
    for gusto in gustos.values():
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
    total_llamados_perdidos = []
    total_llamados_rechazados = []
    total_pizzas_descartadas = []
    total_llamados_atendidos = []
    total_pizzas_producidas = []
    camionetas, producidas = crear_camionetas(gustos)
    produccion_inicial = len(producidas)
    for i in range(EXPERIMENTOS):
        llamados_perdidos = []
        llamados_rechazados = []
        llamados_atendidos = []
        pizzas_descartadas = []
        pizzas_producidas = []
        #pizzas_producidas.extend(producidas)
        for j in range(CORRIDAS):
            print "E: %d, C: %d" % (i, j)
            llamadas = crear_llamadas(gustos)
            eventos = crear_evento_llamada([], llamadas)
            print "LISTADO DE EVENTOS DE LLAMADA"
            for e in eventos:
                print e
            #break

            reloj = singleton(Reloj)
            reloj.set_reloj(0)
            k = 0
            while len(eventos) > 0:            
                reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                evento_atendido = False #Flag de que atendi el evento
                nuevo_evento = None
                print "Eventos no atendidos aun: ", len(eventos)
                if eventos[k].tipo == "llamada_cliente":
                    llamado = eventos[k].objeto
                    x, y = llamado.get_ubicacion()
                    if distancia_entre_puntos(x, y, 0, 0) > MAX_DISTANCIA:
                        print "fuera de rango - pedido rechazado"
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
                                    if c.tiene_gusto(gusto):
                                        c.atender_llamado(llamado)
                                        reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), llamado.get_hora()))
                                        nuevo_evento = Evento(c, reloj.get_reloj(), "atencion_pedido")
                                        evento_atendido = True
                                        break
                                    else:
                                        if cambia_pedido():
                                            print "Cliente cambia pedido"
                                            gustos_disponibles = c.get_gustos()
                                            gusto = gustos_disponibles[0]
                                            llamado.set_gusto(gusto)
                                            c.atender_llamado(llamado)
                                            reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), llamado.get_hora()))
                                            nuevo_evento = Evento(c, reloj.get_reloj(), "atencion_pedido")
                                            evento_atendido = True
                                        else:
                                            print "Mando camioneta %d a recargar" % (c.id)
                                            t_viaje = c.tiempo_a_punto(0, 0)
                                            c.atender_llamado(llamado)
                                            nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje, "inicio_recarga")
                        if evento_atendido is False:
                            print "Llamado %d en espera" % (eventos[k].objeto.id)
                            
                elif eventos[k].tipo == "atencion_pedido":
                    c = eventos[k].objeto
                    x, y = c.llamada.ubicacion
                    t_viaje = c.tiempo_a_punto(x, y)
                    #print "Soy la camioneta %d y atiendo un Pedido" % (c.id)
                    nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje, "entrega_pedido")
                    evento_atendido = True
                elif eventos[k].tipo == "entrega_pedido":
                    current = eventos[k]
                    c = current.objeto
                    if c.llamada.timeout(reloj.get_reloj()):
                        llamados_perdidos.append(c.llamada)
                        print "llamada %d perdida por timeout" % (c.llamada.id)
                        evento_atendido = True
                    c.fin_atencion()
                    print "Pizza entregada por %d" % (c.id)
                    llamados_atendidos.append(c.llamada)
                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                    evento_atendido = True

                elif eventos[k].tipo == "inicio_recarga":
                    c = eventos[k].objeto
                    tenia = len(c.pizzas)
                    t_carga, malas, producidas = c.recargar(c.llamada.gusto, gustos, reloj.get_reloj())
                    pizzas_descartadas.extend(malas)
                    pizzas_producidas.extend(producidas)
                    print "Soy la camioneta %d. Tenia %d, Descarte %d y recargue %d pizzas" % (c.id, tenia, len(malas), len(producidas))
                    nuevo_evento = Evento(c, reloj.get_reloj()+t_viaje+t_carga, "fin_recarga")
                    evento_atendido = True
                elif eventos[k].tipo == "fin_recarga":
                    #reloj = singleton(Reloj)
                    c = eventos[k].objeto
                    reloj.set_reloj(avanzar_reloj(reloj.get_reloj(), eventos[k].tiempo))
                    #c.finalizar_carga(singleton(Reloj).get_reloj())
                    c.finalizar_carga(reloj.get_reloj())
                    evento_atendido = True

                if not nuevo_evento is None:
                    #print "Son las %d y creo el evento %s para las %d" % (reloj.get_reloj(), nuevo_evento.tipo, nuevo_evento.tiempo)
                    eventos = agregar_evento(eventos, nuevo_evento)

                if evento_atendido:
                    eventos = eliminar_evento(eventos, eventos[k])
                    k = 0
                    #print "Evento fue atendido y lo elimino de la lista de eventos. Me quedan %d Eventos por atender" % (len(eventos))
                    #for e in eventos:
                    #    print e
                else:
                    k += 1
            print "Fin ejecucion - eventos en cola: ", len(eventos)
        total_llamados_perdidos.append(len(llamados_perdidos))
        total_llamados_rechazados.append(len(llamados_rechazados))
        total_pizzas_descartadas.append(len(pizzas_descartadas))
        total_llamados_atendidos.append(len(llamados_atendidos))
        total_pizzas_producidas.append(len(pizzas_producidas))
    print "Resultados de la corrida"
    print "Promedio %.2f Cantidad de Pizzas producidas: %d" %(np.average(total_pizzas_producidas), np.sum(total_pizzas_producidas)+produccion_inicial )
    print "Promedio %.2f Cantidad de Pizzas descartadas: %d" %(np.average(total_pizzas_descartadas) , np.sum(total_pizzas_descartadas))
    print "Promedio %.2f Cantidad de llamados atendidos: %d" %(np.average(total_llamados_atendidos) , np.sum(total_llamados_atendidos))
    print "Promedio %.2f Cantidad de llamados perdidos: %d" %(np.average(total_llamados_perdidos), np.sum(total_llamados_perdidos))
    print "Promedio %.2f Cantidad de llamados rechazados: %d" %(np.average(total_llamados_rechazados), np.sum(total_llamados_rechazados))
    print "Contenido de stock en camionetas: ", (np.sum(total_pizzas_producidas)+produccion_inicial) - np.sum(total_pizzas_descartadas) - np.sum(total_llamados_atendidos)
    
if __name__ == '__main__':
    main()
