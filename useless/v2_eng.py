#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import simpy


class Task(object):
    """ Has an id i.e.: 'E',
        duration i.e.: 5
        a list with Task that precede the current
    """
    def __init__(self, id, duration, env, previousTasks=[]):
        self.id = id
        self.duration = duration
        self.env = env
        self.completed = env.event()
        self.completed.succeed(False)
        self.action = env.process(self.run())
        if previousTasks is None:
            self.previousTasks = []
        else:
            self.previousTasks = previousTasks

    def run(self):
        print "Current Task running", self.id
        while self.can_execute() and not self.completed.value:
            print "Run(): Starting task %s at time %s" % (self.id, self.env.now)
            yield self.env.timeout(self.duration)
            print "Run(): Completed task %s in time %s" % (self.id, self.env.now)
            self.completed.succeed(True)

    def can_execute(self):
        result = True
        #print "Current Task running", self.id
        for task in self.previousTasks:
            if not task.completed.processed:
                result = False
                break
        #print "result ", result
        return result

if __name__ == '__main__':
    env = simpy.Environment()
    taskA = Task('A', 4, env)
    taskB = Task('B', 5, env, [taskA])
    env.run(until=20)
