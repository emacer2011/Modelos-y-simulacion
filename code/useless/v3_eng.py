#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import simpy
from simpy.util import start_delayed
from numpy.random import randint

delays = {}
completed = []
rutas = []


class Task(object):
    """ Has an id i.e.: 'E',
        duration i.e.: 5
        a list with Task that precede the current
    """
    def __init__(self, id, duration, env, soy_final=False, previousTasks=None):
        self.id = id
        self.duration = duration
        self.env = env
        self.soy_final = soy_final
        if previousTasks is None:
            self.previousTasks = []
        else:
            self.previousTasks = previousTasks
        self.action = None

    def run(self):
        while True:
            camino = []
            if delays[self.id] == env.now:
                if self.soy_final:
                    camino = armar_camino(self.previousTasks)
                    camino.append(self.id)
                    camino.sort()
                    rutas.append((camino, delays[self.id]+self.duration))
                #print "---> Soy: %s tiempo: %s" % (self.id, self.env.now)
                yield self.env.timeout(self.duration)
                completed.append(self.id)
                print "Soy: %s duracion: %s" % (self.id, self.duration)
            else:
                if self.id in completed:
                    self.env.exit()


def armar_camino(previas):
    camino = []
    if len(previas) > 0:
        camino.extend(map(lambda x: x.id, previas))
        for previa in previas:
            camino.extend(armar_camino(previa.previousTasks))
    return camino


def agregar_dependencias(previas, duraciones):
    if len(previas) == 0:
        return 0
    else:
        duraciones.extend(map(lambda x: x.duration, previas))
        for previa in previas:
            agregar_dependencias(previa.previousTasks, duraciones)
        return sum(duraciones)


def estimate_delays(tasks):
    result = {}
    for task in tasks:
        durations = []
        total = (agregar_dependencias(task.previousTasks, durations))
        result.update({task.id: total})
    return result


def set_action(tasks):
    for task in tasks:
        if delays[task.id] > 0:
            task.action = start_delayed(task.env, task.run(), delays[task.id])
        else:
            task.action = env.process(task.run())


def camino_critico(rutas):
    critico = []
    duracion = 0
    for ruta in rutas:
        if ruta[1] > duracion:
            critico = ruta[0]
            duracion = ruta[1]
    return critico, duracion


if __name__ == '__main__':
    env = simpy.Environment()
    taskA = Task('A', randint(1, 9), env)
    taskB = Task('B', randint(1, 9), env, previousTasks=[taskA])
    taskC = Task('C', randint(1, 9), env, soy_final=True, previousTasks=[taskB])
    taskD = Task('D', randint(8, 16), env, soy_final=True)
    taskE = Task('E', randint(4, 8), env)
    taskF = Task('F', randint(4, 8), env, soy_final=True, previousTasks=[taskE])
    tasks = [taskA, taskB, taskC, taskD, taskE, taskF]
    delays.update(estimate_delays(tasks))
    set_action(tasks)
    env.run(until=20)
    print "Rutas del proyecto\n", rutas
    critico, duracion = camino_critico(rutas)
    print "Camino critico\n%s\nDuracion minima del proyecto:%s" % (critico, duracion)
