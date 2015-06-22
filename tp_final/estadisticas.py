#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np


class Estadisticas(object):

    def __init__(self):
        self.produccion_inicial = 0
        self.pizzas_producidas = 0
        self.pizzas_descartadas = 0
        self.llamados_atendidos = 0
        self.llamados_perdidos = 0
        self.llamados_rechazados = 0

    def set_produccion(self, produccion_inicial, total_pizzas_producidas, total_pizzas_descartadas):
        self.produccion_inicial = produccion_inicial
        self.pizzas_producidas = total_pizzas_producidas
        self.pizzas_descartadas = total_pizzas_descartadas

    def get_pizzas_producidas(self):
        ''' devuelve promedio y total de Pizzas producidas '''
        return np.average(self.pizzas_producidas), np.sum(self.pizzas_producidas) + self.produccion_inicial

    def get_pizzas_descartadas(self):
        ''' devuelve promedio, total de Pizzas descartadas y Porcentaje sobre el total de Producidas '''
        return np.average(self.pizzas_descartadas) , np.sum(self.pizzas_descartadas), (np.sum(self.pizzas_descartadas)/(np.sum(self.pizzas_producidas)+self.produccion_inicial))*100

    def set_llamadas(self, total_llamados_atendidos, total_llamados_perdidos, total_llamados_rechazados):
        self.llamados_atendidos = total_llamados_atendidos
        self.llamados_perdidos = total_llamados_perdidos
        self.llamados_rechazados = total_llamados_rechazados

    def get_llamados_total(self):
        ''' devuelve promedio y total de llamadas en Total '''
        return (np.average(self.llamados_atendidos)+np.average(self.llamados_perdidos)+np.average(self.llamados_rechazados) , np.sum(self.llamados_atendidos)+np.sum(self.llamados_perdidos)+np.sum(self.llamados_rechazados))

    def get_llamados_atendidos(self):
        ''' devuelve promedio, total de llamados atentdidos y Porcentaje sobre el total de llamados '''
        return (np.average(self.llamados_atendidos) , np.sum(self.llamados_atendidos), np.sum(self.llamados_atendidos) / self.get_llamados_total()[1]*100)

    def get_llamados_perdidos(self):
        ''' devuelve promedio, total de llamados perdidos y Porcentaje sobre el total de llamados '''
        return (np.average(self.llamados_perdidos) , np.sum(self.llamados_perdidos), np.sum(self.llamados_perdidos) / self.get_llamados_total()[1]*100)

    def get_llamados_rechazados(self):
        ''' devuelve promedio, total de llamados rechazados y Porcentaje sobre el total de llamados '''
        return (np.average(self.llamados_rechazados) , np.sum(self.llamados_rechazados), np.sum(self.llamados_rechazados) / self.get_llamados_total()[1]*100)


