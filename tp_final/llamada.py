#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np


class Llamada(object):
    """docstring for Llamada"""
    def __init__(self, hora, gusto):
        self.X = np.random.Normal(0, 1000/3)
        self.Y = np.random.Normal(0, 1000/3)
        super(Llamada, self).__init__()
        self.hora = hora
        self.gusto = gusto
        self.ubicacion = (self.X, self.Y)

    def get_ubicacion(self):
        return self.ubicacion

    def get_gusto(self):
        return self.gusto

    def get_hora(self):
        return self.hora
