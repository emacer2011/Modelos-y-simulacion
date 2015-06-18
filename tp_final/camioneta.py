#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import math
from pizza import Pizza
from reloj import Reloj
import numpy as np


class Camioneta(object):
    """docstring for Camioneta"""
    def __init__(self):
        super(Camioneta, self).__init__()
        self.ocupado = False
        self.ubicacion = (0, 0)
        self.distancia_rec = 0
        self.pizzas = {}
        self.VC_MAX = 500  # mts/min = 30km/h
        self.MAX_PIZZAS = 40
        self.llamada = None  # referencia al obj Llamada que atiende
        self.tiempo_entre_rec = []
        self.ultima_rec = 0

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
        r = Reloj()
        p = Pizza(gusto, r.get_valor())
        self.pizzas[gusto].append(p)
        return p

    def quitar_pizzas_vencidas(self):
        malas = (pizza for pizza in self.pizzas if pizza.get_estado() is False)  # Devuelve las que estan en mal estado
        buenas = (pizza for pizza in self.pizzas if pizza.get_estado() is True)
        self.pizzas = buenas
        return malas

    def cargar(self, gusto_principal, gustos):
        """Devuelve el tiempo de carga y las pizzas en mal estado"""
        producidas = []
        self.ocupado = True
        malas = self.quitar_pizzas_vencidas()
        pizza = self.agregar_pizza(gusto_principal)
        producidas.append(pizza)
        while len(self.get_pizzas()) < self.MAX_PIZZAS:
            key = np.random.randint(1, len(gustos))
            prob = np.random.binomial(1, gustos[key].get_probabilidad())
            if prob:
                pizza = self.agregar_pizza(gustos[key])
                producidas.append(pizza)
                print "cargo pizza de gusto: %s", gustos[key].nombre
        return np.random.Exponential(10), malas

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
        return set(gustos)

    def finalizar_carga(self, reloj):
        self.tiempo_entre_rec.append(reloj.get_reloj()-self.ultima_rec)
        self.ultima_rec = reloj.get_reloj()
        self.ocupado = False
