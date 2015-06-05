#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import simpy


class Tarea(object):
    """ Clase representante de una tarea
        Necesita un identificador p.ej: 'E',
        una duracion en dias. p.ej: 5
        una lista con los objetos Tarea que preceden a la tarea actual
    """
    def __init__(self, idTarea, duracionDias, env, precedentes=[]):
        self.idTarea = idTarea
        self.duracionDias = duracionDias
        self.env = env
        self.precedentes = precedentes
        self.termino = env.event()
        self.action = env.process(self.ejecutar_tarea())

    def ejecutar_tarea(self):
        while self.puedo_correr() and not self.termino.triggered:
            yield self.env.timeout(self.duracionDias)
            print "Termino tarea %s en dia %s" % (self.idTarea, self.env.now)
            self.termino.succeed(True)

    def puedo_correr(self):
        resultado = True
        print "idTarea %s" % self.idTarea
        for tarea in self.precedentes:
            if not tarea.termino.triggered:
                resultado = False
                break
        return resultado

env = simpy.Environment()
TareaA = Tarea('A', 4, env)
TareaB = Tarea('B', 5, env, [TareaA])
env.run(until=20)
