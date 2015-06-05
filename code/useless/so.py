#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import simpy
from simpy.util import start_delayed
from numpy.random import randint

delays = {}
completed = []


class Task(object):
    """ Has an id i.e.: 'E',
        duration i.e.: 5
        a list with Task that precede the current
    """
    def __init__(self, id, duration, env, previousTasks=None):
        self.id = id
        self.duration = duration
        self.env = env
        if previousTasks is None:
            self.previousTasks = []
        else:
            self.previousTasks = previousTasks
        self.action = None

    def run(self):
        while True:
            if delays[self.id] == self.env.now:
                print "Start task: %s at time: %s" % (self.id, self.env.now)
                yield self.env.timeout(self.duration)
                completed.append(self.id)
                print "Finish task: %s at time: %s" % (self.id, self.env.now)
            else:
                if self.id in completed:
                    self.env.exit()


def add_precedences(prevTask, durations):
    if len(prevTask) == 0:
        return 0
    else:
        durations.extend(map(lambda x: x.duration, prevTask))
        for prev in prevTask:
            add_precedences(prev.previousTasks, durations)
        return sum(durations)


def estimate_delays(tasks):
    result = {}
    for task in tasks:
        durations = []
        total = (add_precedences(task.previousTasks, durations))
        result.update({task.id: total})
    return result


def set_action(tasks):
    for task in tasks:
        if delays[task.id] > 0:
            task.action = start_delayed(task.env, task.run(), delays[task.id])
        else:
            task.action = env.process(task.run())

if __name__ == '__main__':
    env = simpy.Environment()
    taskA = Task('A', randint(1, 9), env)
    taskB = Task('B', randint(1, 9), env, previousTasks=[taskA])
    taskC = Task('C', randint(1, 9), env, previousTasks=[taskB])
    tasks = [taskA, taskB, taskC]
    delays.update(estimate_delays(tasks))
    set_action(tasks)
    env.run(until=20)
