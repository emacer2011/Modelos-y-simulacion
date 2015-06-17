#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


class Evento(object):
    def __init__(self, objeto, tiempo, tipo):
        self.objeto = objeto
        self.tiempo = tiempo
        self.tipo = tipo

    def __str__(self):
        return "(%d){%s - %d}" % (self.tiempo, self.objeto.__class__.__name__.title(), self.objeto.id)
