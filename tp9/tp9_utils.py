from __future__ import division
import numpy as np


def agregar_evento(eventos, evento):
    eventos.append(evento)
    eventos.sort(key=lambda e: e.tiempo)
    return eventos


def eliminar_evento(eventos, evento):
    eventos.remove(evento)
    eventos.sort(key=lambda e: e.tiempo)
    return eventos


def generar_cliente(reloj):
    llegada = reloj + np.random.exponential(20)
    cliente = Cliente(llegada)
    return cliente


class Evento(object):
    def __init__(self, objeto, tiempo, tipo):
        self.objeto = objeto
        self.tiempo = tiempo
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
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_atencion = 0
        self.tiempo_salida = 0

    def generar_evento_llegada(self, eventos):
        agregar_evento(eventos, Evento(self, self.tiempo_llegada, 'llegada_cliente'))
        return eventos

    def tiempo_espera(self):
        return self.tiempo_atencion - self.tiempo_llegada
