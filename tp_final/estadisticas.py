#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import matplotlib as mpl
mpl.rcParams['font.size'] = 9.0
import matplotlib.pyplot as plt

class Estadisticas(object):

    def __init__(self):
        #self.produccion_inicial = 0
        self.pizzas_producidas = 0
        self.pizzas_descartadas = 0
        self.llamados_atendidos = 0
        self.llamados_perdidos = 0
        self.llamados_rechazados = 0
        self.posiciones_x = None
        self.posiciones_y = None

    def set_produccion(self, total_pizzas_producidas, total_pizzas_descartadas):
        #self.produccion_inicial = produccion_inicial
        self.pizzas_producidas = total_pizzas_producidas
        self.pizzas_descartadas = total_pizzas_descartadas

    def get_pizzas_producidas(self):
        ''' devuelve promedio y total de Pizzas producidas '''
        return np.average(self.pizzas_producidas), np.sum(self.pizzas_producidas) #+ self.produccion_inicial


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

    def mostrar_estadisticas(self, detalle_prod, detalle_desc):
        # Detalle de llamadas
        p_atendidos = self.get_llamados_atendidos()[2]
        p_rechazados = self.get_llamados_rechazados()[2]
        p_perdidos = self.get_llamados_perdidos()[2]
        llamadas = [self.get_llamados_atendidos()[1], self.get_llamados_rechazados()[1], self.get_llamados_perdidos()[1]]
        labels_llamadas = [u'Atendidas %.2f %%' % p_atendidos, u'Rechazadas %.2f %%' % p_rechazados, u'Perdidas %.2f %%' % p_perdidos]
        plt.figure(facecolor='white')
        plt.subplot(2, 2, 1)
        plt.pie(llamadas, labels = labels_llamadas)  # Dibuja un gráfico de quesitos
        plt.title(u'Porcentaje de llamadas')
        #plt.savefig('fig0.png')

        
        # Estado de las pizzas
        plt.subplot(2, 2, 2)
        stock_restante = self.get_stock_restante()
        descartadas = self.get_pizzas_descartadas()[1]
        pizzas = [self.get_llamados_atendidos()[1], descartadas, stock_restante ]
        entregadas = self.get_llamados_atendidos()[1]/self.get_pizzas_producidas()[1]
        descartadas = self.get_pizzas_descartadas()[2]
        stock_restante = stock_restante/self.get_pizzas_producidas()[1]*100
        labels_pizzas = [u'Entregadas %.2f %%' % (entregadas*100), 
                        u'Descartadas %.2f %%' % (descartadas), 
                        u'En stock %.2f %%' % (stock_restante)]
        plt.pie(pizzas, labels = labels_pizzas)
        plt.title(u'Porcentaje de pizzas (Gral.)')
        #plt.savefig('fig1.png')

        # Detalle de produccion de pizzas
        plt.subplot(2, 2, 3)
        porcentajes = [] 
        labels_gustos = []
        for k, v in detalle_prod.iteritems():
            porcentaje =  v/self.get_pizzas_producidas()[1]*100
            labels_gustos.append('%s %.2f %%' % (k, porcentaje)),
        plt.pie(detalle_prod.values(), labels = labels_gustos)
        plt.title(u'Detalle de pizzas producidas')
        #plt.savefig('fig2.png')
        
        
        
        plt.subplot(2, 2, 4)
        d_anchoas = detalle_desc['Anchoas']
        d_calabresa = detalle_desc['Calabresa']
        d_napolitana = detalle_desc['Napolitana']
        d_especial = detalle_desc['Especial']
        d_muzza = detalle_desc['Muzza']
        pizzas = [d_anchoas, d_muzza, d_napolitana, d_especial, d_calabresa]
        labels_pizzas = [u'Anchoas %.2f %%' % (d_anchoas/self.get_pizzas_descartadas()[1]*100),
                        u'Muzza %.2f %%' % (d_muzza/self.get_pizzas_descartadas()[1]*100), 
                        u'Napolitana %.2f %%' % (d_napolitana/self.get_pizzas_descartadas()[1]*100),
                        u'Especial %.2f %%' % (d_especial/self.get_pizzas_descartadas()[1]*100),
                        u'Calabresa %.2f %%' % (d_calabresa/self.get_pizzas_descartadas()[1]*100)]
        plt.pie(pizzas, labels = labels_pizzas)
        plt.title(u'Porcentaje de descartes')
        #plt.savefig('fig3.png')
        plt.show()

        


        # Dispersion de llamadas
        x = np.array(self.posiciones_x)
        y = np.array(self.posiciones_y)
        plt.grid(True)
        plt.scatter(x,y)
        plt.scatter(0,0, color="red")
        plt.title(u'Dispersion de llamadas')
        plt.savefig('fig4.png')
        plt.show()
