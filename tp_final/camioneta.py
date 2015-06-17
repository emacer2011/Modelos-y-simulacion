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

    def get_estado(self):
        return self.ocupado

    def set_estado(self, new_ocupado):
        self.ocupado = new_ocupado

    def get_pizzas(self):
        return self.pizzas

    def agregar_pizzas(self, cantidad, gusto):
        r = Reloj()
        for i in range(cantidad):
            p = Pizza(gusto, r.get_valor())
            self.pizzas[gusto].append(p)

    def quitar_pizzas_vencidas(self):
        malas = (pizza for pizza in self.pizzas if pizza.get_estado() is False)  # Devuelve las que estan en mal estado
        buenas = (pizza for pizza in self.pizzas if pizza.get_estado() is True)
        self.pizzas = buenas
        return malas

    def carga(self):
        """Devuelve el tiempo de carga"""
        self.ocupado = True
        return np.random.Exponential(10)
