from simpy import Environment
from simpy.util import start_delayed


def my_process(env, x):
    print('%s, %s' % (env.now, x))
    yield env.timeout(1)

env = Environment()
proc1 = env.process(my_process(env, 2))
proc2 = start_delayed(env, my_process(env, 3), 5)
env.run(until=10)
