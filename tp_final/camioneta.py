#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import math
from pizza import Pizza
from reloj import *
import numpy as np


class Camioneta(object):
    def __init__(self, pizzas=None, tiempo_entre_rec=None):
        self.id = id(self)
        self.ocupado = False
        self.ubicacion = (0, 0)
        self.distancia_rec = 0
        self.VC_MAX = 500  # mts/min = 30km/h
        self.MAX_PIZZAS = 40
        self.llamada = None  # referencia al obj Llamada que atiende
        self.ultima_rec = 0
        if pizzas is None:
            self.pizzas = []
        if tiempo_entre_rec is None:
            self.tiempo_entre_rec = []
        
    def get_ubicacion(self):
        return self.ubicacion

    def set_ubicacion(self, new_ubicacion):
        self.ubicacion = new_ubicacion

    def distancia_a_punto(self, x2, y2):
        """Devuelve distancia en metros"""
        x1, y1 = self.get_ubicacion()
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def tiempo_a_punto(self, x, y):
        """Devuelve tiempo en minutos"""
        return (int) (self.distancia_a_punto(x, y) / self.VC_MAX)

    def get_ocupado(self):
        return self.ocupado

    def get_pizzas(self):
        return self.pizzas

    def agregar_pizza(self, gusto):
        reloj = singleton(Reloj).get_reloj()
        pizza = Pizza(gusto, reloj)
        self.pizzas.append(pizza)
        return pizza

    def quitar_pizzas_vencidas(self, hora):
        malas = filter(lambda p: p.get_estado(hora) is False, self.pizzas)
        buenas = filter(lambda p: p.get_estado(hora) is True, self.pizzas)
        self.pizzas = buenas
        return malas

    def cargar(self, gustos):
        producidas = []
        while len(self.pizzas) < self.MAX_PIZZAS:
            key = np.random.randint(1, len(gustos))
            prob = np.random.binomial(1, gustos[key].get_probabilidad())
            if prob:
                pizza = self.agregar_pizza(gustos[key])
                producidas.append(pizza)
        return producidas

    def recargar(self, gusto_principal, gustos, hora):
        """Devuelve el tiempo de carga, las pizzas en mal estado, las pizzas producidas"""
        producidas = []
        self.ocupado = True
        #Me situo en punto 0,0
        self.set_ubicacion((0,0))
        malas = self.quitar_pizzas_vencidas(hora)
        if len(self.pizzas) == self.MAX_PIZZAS:
            self.pizzas.remove(self.pizzas[0])
        pizza = self.agregar_pizza(gusto_principal)
        producidas.append(pizza)
        producidas.extend(self.cargar(gustos))
        return np.random.exponential(10), malas, producidas

    def tiene_gusto(self, gusto):
        for p in self.get_pizzas():
            if p.gusto.nombre == gusto.nombre and p.estado is True:
                return True
        return False

    def atender_llamado(self, llamado):
        self.ocupado = True
        self.llamada = llamado
        x, y = llamado.get_ubicacion()
        self.distancia_rec += self.distancia_a_punto(x, y)
        print "[%d] soy camioneta %d y llevo recorrido %d km" % (singleton(Reloj).get_reloj(), self.id, self.distancia_rec/1000)

    def fin_atencion(self):
        for p in self.get_pizzas():
            if p.estado and p.gusto.nombre == self.llamada.gusto.nombre:
                self.get_pizzas().remove(p)
                break
        self.set_ubicacion(self.llamada.ubicacion)
        #self.llamada = None
        self.ocupado = False

    def get_gustos(self):
        gustos = []
        for p in self.get_pizzas():
            if p.estado:
                gustos.append(p.gusto)
        set_gustos = set(gustos)
        lista_gustos = list(set_gustos)
        return lista_gustos

    def finalizar_carga(self, reloj):
        self.tiempo_entre_rec.append(reloj-self.ultima_rec)
        self.ultima_rec = reloj
        #self.ocupado = False
