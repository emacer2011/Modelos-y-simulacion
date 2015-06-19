#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


class Gusto(object):
    """docstring for Gusto"""
    def __init__(self, nombre, probabilidad):
        super(Gusto, self).__init__()
        self.nombre = nombre
        self.probabilidad = probabilidad

    def get_probabilidad(self):
        return self.probabilidad


class Pizza(object):
    """docstring for Pizza"""
    def __init__(self, gusto, creacion):
        super(Pizza, self).__init__()
        self.gusto = gusto
        self.creacion = creacion
        self.vencimiento = 60
        self.estado = True  # True = Buen estado

    def get_estado(self, hora):
        resto_tiempo = hora - self.creacion
        if (resto_tiempo > self.vencimiento):
            return False
        else:
            return True