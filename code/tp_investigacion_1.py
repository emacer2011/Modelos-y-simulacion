#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import simpy
tareas = {}


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
        self.action = env.process(self.run())
        self.precedentes = precedentes

    def run(self):
        global tareas
        while True:
            while self.puede_correr(self.precedentes) and not tareas[self.idTarea]:
                print 'Comienza la tarea %s en dia: %d' % (self.idTarea, self.env.now)
                yield self.env.process(self.ejecutar(self.duracionDias))
                print 'Finaliza la tarea %s en dia: %d' % (self.idTarea, self.env.now)
                tareas.update({self.idTarea: True})

    def puede_correr(self, precedentes):
        global tareas
        resultado = True
        for tarea in precedentes:
            print "precedente: %s, termino? %s" % (tarea.idTarea, tareas[tarea.idTarea])
            if tareas[tarea.idTarea] == False:
                resultado = False
                break
        return resultado

    def ejecutar(self, duracion):
        yield self.env.timeout(duracion)

if __name__ == '__main__':
    env = simpy.Environment()
    tareaA = Tarea('A', 4, env)
    tareaB = Tarea('B', 5, env)
    tareaC = Tarea('C', 3, env, [tareaA])
    tareas.update({tareaA.idTarea: False,
                    tareaB.idTarea: False,
                    tareaC.idTarea: False})
    env.run(until=30)
