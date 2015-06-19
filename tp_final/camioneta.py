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

    def distancia_a_punto(self, x, y):
        """Devuelve distancia en metros"""
        return math.sqrt(x**2+y**2)

    def tiempo_a_punto(self, x, y):
        """Devuelve tiempo en minutos"""
        return (self.VC_MAX * self.distancia_a_punto(x, y))

    def get_ocupado(self):
        return self.ocupado

    def get_pizzas(self):
        return self.pizzas

    def agregar_pizza(self, gusto):
        reloj = singleton(Reloj).get_reloj()
        pizza = Pizza(gusto, reloj)
        self.pizzas.append(pizza)
        return pizza

    def quitar_pizzas_vencidas(self):
        malas = filter(lambda p: p.estado is False, self.pizzas)
        buenas = filter(lambda p: p.estado is True, self.pizzas)
        self.pizzas = buenas
        return malas

    def cargar(self, gustos):
        producidas = []
        #print "soy %d y tengo %d pizzas" % (self.id, len(self.pizzas))
        while len(self.pizzas) < self.MAX_PIZZAS:
            key = np.random.randint(1, len(gustos))
            prob = np.random.binomial(1, gustos[key].get_probabilidad())
            if prob:
                pizza = self.agregar_pizza(gustos[key])
                producidas.append(pizza)
                #print "cargo pizza de gusto: ", gustos[key].nombre
        return producidas

    def recargar(self, gusto_principal, gustos):
        """Devuelve el tiempo de carga, las pizzas en mal estado, las pizzas producidas"""
        producidas = []
        self.ocupado = True
        malas = self.quitar_pizzas_vencidas()
        if len(self.pizzas) == self.MAX_PIZZAS:
            self.pizzas.remove(self.pizzas[0])
            pizza = self.agregar_pizza(gusto_principal)
            print "descarto porque estoy lleno"
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

    def fin_atencion(self):
        for p in self.get_pizzas():
            if p.estado and p.gusto.nombre == self.llamada.gusto.nombre:
                self.get_pizzas().pop(p)
                break
        self.set_ubicacion(self.llamada.ubicacion)
        self.llamada = None
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
        self.ocupado = False
