#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import simpy
from simpy.util import start_delayed
from numpy.random import randint

delays = {}
completadas = []
rutas = []


class Tarea(object):
    """ Tiene un id p.ej: 'E',
        duracion p.ej: 5
        una lista con las tareas que preceden a la actual
    """
    def __init__(self, id, duracion, env, soy_final=False, previas=None):
        self.id = id
        self.duracion = duracion
        self.env = env
        self.soy_final = soy_final
        if previas is None:
            self.previas = []
        else:
            self.previas = previas
        self.action = None

    def run(self):
        while True:
            camino = []
            if delays[self.id] == env.now:
                if self.soy_final:
                    camino = armar_camino(self.previas)
                    camino.append(self.id)
                    camino.sort()
                    rutas.append((camino, delays[self.id]+self.duracion))
                #print "---> Soy: %s tiempo: %s" % (self.id, self.env.now)
                yield self.env.timeout(self.duracion)
                completadas.append(self.id)
                print "Soy: %s duracion: %s" % (self.id, self.duracion)
            else:
                if self.id in completadas:
                    self.env.exit()


def armar_camino(previas):
    """
        Arma el camino critico con los identificadores
        de cada tarea.
    """
    camino = []
    if len(previas) > 0:
        camino.extend(map(lambda x: x.id, previas))
        for previa in previas:
            camino.extend(armar_camino(previa.previas))
    return camino


def agregar_precedencias(previas, duraciones):
    """
        Calcula la duracion de una tarea
        teniendo en cuenta la duracion de las tareas precedentes
    """
    if len(previas) == 0:
        return 0
    else:
        duraciones.extend(map(lambda x: x.duracion, previas))
        for previa in previas:
            agregar_precedencias(previa.previas, duraciones)
        return sum(duraciones)


def estimar_delays(tareas):
    """
        Estima el tiempo de arranque para cada tarea
    """
    resultado = {}
    for tarea in tareas:
        durations = []
        total = (agregar_precedencias(tarea.previas, durations))
        resultado.update({tarea.id: total})
    return resultado


def set_action(tasks):
    """
        Setea el atributo action de cada tarea
        dependiendo de las precedencias de cada una
    """
    for task in tasks:
        if delays[task.id] > 0:
            task.action = start_delayed(task.env, task.run(), delays[task.id])
        else:
            task.action = env.process(task.run())


def camino_critico(rutas):
    """Determina el camino critico y su duracion"""
    critico = []
    duracion = 0
    for ruta in rutas:
        if ruta[1] > duracion:
            critico = ruta[0]
            duracion = ruta[1]
    return critico, duracion


if __name__ == '__main__':
    env = simpy.Environment()
    tareaA = Tarea('A', randint(1, 9), env)
    tareaB = Tarea('B', randint(1, 9), env, previas=[tareaA])
    tareaC = Tarea('C', randint(1, 9), env, soy_final=True, previas=[tareaB])
    tareaD = Tarea('D', randint(8, 16), env, soy_final=True)
    tareaE = Tarea('E', randint(4, 8), env)
    tareaF = Tarea('F', randint(4, 8), env, soy_final=True, previas=[tareaE])
    tareas = [tareaA, tareaB, tareaC, tareaD, tareaE, tareaF]
    delays.update(estimar_delays(tareas))
    set_action(tareas)
    env.run(until=20)
    print "Rutas del proyecto\n", rutas
    critico, duracion = camino_critico(rutas)
    print "Camino critico\n%s\nDuracion minima del proyecto:%s" % (critico, duracion)
