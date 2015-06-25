#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

class Estadisticas(object):

    def __init__(self):
        self.produccion_inicial = 0
        self.pizzas_producidas = 0
        self.pizzas_descartadas = 0
        self.llamados_atendidos = 0
        self.llamados_perdidos = 0
        self.llamados_rechazados = 0
        self.posiciones_x = None
        self.posiciones_y = None

    def set_produccion(self, pizzas_producidas, pizzas_descartadas):
        self.pizzas_producidas = pizzas_producidas
        self.pizzas_descartadas = pizzas_descartadas

    def get_pizzas_producidas(self):
        ''' devuelve promedio y total de Pizzas producidas '''
        return np.average(self.pizzas_producidas), np.sum(self.pizzas_producidas)


    def get_pizzas_descartadas(self):
        ''' devuelve promedio, total de Pizzas descartadas y Porcentaje sobre el total de Producidas '''
        return np.average(self.pizzas_descartadas) , np.sum(self.pizzas_descartadas), (np.sum(self.pizzas_descartadas)/(np.sum(self.pizzas_producidas))*100)

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

    def get_stock_restante(self):
        return (np.sum(self.pizzas_producidas)) - np.sum(self.pizzas_descartadas) - np.sum(self.llamados_atendidos)

    def set_posiciones(self, x, y):
        self.posiciones_x = x
        self.posiciones_y = y

    def mostrar_estadisticas(self, detalle):
        # Detalle de llamadas
        p_atendidos = self.get_llamados_atendidos()[2]
        p_rechazados = self.get_llamados_rechazados()[2]
        p_perdidos = self.get_llamados_perdidos()[2]
    
        llamadas = [self.llamados_atendidos, self.llamados_rechazados, self.llamados_perdidos]
        labels_llamadas = [u'Atendidas %.2f %%' % p_atendidos, u'Rechazadas %.2f %%' % p_rechazados, u'Perdidas %.2f %%' % p_perdidos]
        plt.figure(facecolor='white')
        plt.subplot(2, 2, 1)
        plt.pie(llamadas, labels = labels_llamadas)  # Dibuja un gráfico de quesitos
        plt.title(u'Porcentaje de llamadas')

        
        # Estado de las pizzas
        plt.subplot(2, 2, 2)
        stock_restante = self.get_stock_restante()
        pizzas = [self.get_llamados_atendidos()[1], self.pizzas_descartadas[0], stock_restante ]
        entregadas = self.get_llamados_atendidos()[1]/self.get_pizzas_producidas()[1]
        stock_restante = stock_restante/self.get_pizzas_producidas()[1]*100
        descartadas = self.get_pizzas_descartadas()[2]
        labels_pizzas = [u'Entregadas %.2f %%' % (entregadas*100), 
                        u'Descartadas %.2f %%' % (descartadas), 
                        u'En stock %.2f %%' % (stock_restante)]
        plt.pie(pizzas, labels = labels_pizzas)
        plt.title(u'Porcentaje de pizzas (Gral.)')


        # Dispersion de llamadas
        plt.subplot(2, 2, 3)
        x = np.array(self.posiciones_x)
        y = np.array(self.posiciones_y)
        plt.grid(True)
        plt.scatter(x,y)
        plt.scatter(0,0, color="red")
        plt.title(u'Dispersion de llamadas')


        # Detalle de produccion de pizzas
        plt.subplot(2, 2, 4)
        porcentajes = [] 
        for i in range(len(detalle)):
            porcentajes.append(detalle[i]/self.get_pizzas_producidas()[1]*100)
        labels_gustos = [u'Anchoas %.2f %%' % porcentajes[0],
                        u'Muzza %.2f %%' % porcentajes[1] , 
                        u'Napolitana %.2f %%' % porcentajes[2], 
                        u'Especial %.2f %%' % porcentajes[3], 
                        u'Calabresa %.2f %%' % porcentajes[4]]
        plt.pie(detalle, labels = labels_gustos)
        plt.title(u'Detalle de pizzas producidas')
        
        plt.show()
