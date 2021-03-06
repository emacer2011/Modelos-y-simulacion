#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np


class Llamada(object):
    """docstring for Llamada"""
    def __init__(self, hora, gusto):
        self.id = id(self)
        self.X = np.random.normal(0, 2500/3)
        self.Y = np.random.normal(0, 2500/3)
        # self.X = np.random.randint(-1000, 1000)
        # self.Y = np.random.randint(-1000, 1000)
        self.hora = hora
        self.gusto = gusto
        self.ubicacion = (self.X, self.Y)
        self.atendida = False

    def get_ubicacion(self):
        return self.ubicacion

    def get_gusto(self):
        return self.gusto

    def get_hora(self):
        return self.hora

    def set_gusto(self, nuevo_gusto):
        self.gusto = nuevo_gusto

    def timeout(self, hora_actual):
        return hora_actual - self.hora >= 30

    def is_atendida():
        return self.atendida
