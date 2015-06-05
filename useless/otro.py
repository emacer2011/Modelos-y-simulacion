#at time 20 generate a request event
import simpy
class TrainStation:
    def __init__(self,env):
        self.env= env
        self.request_event = env.event()
        self.request_receiver_process = env.process(self.receive_request())
        self.request_producer_process = env.process(self.produce_request())

    def produce_request(self):
        yield self.env.timeout(20)
        self.request_event.succeed()
        self.request_event = self.env.event()

    def receive_request(self):
        print("Waiting for request at time: {0}".format(env.now))
        yield self.request_event
        print("Request received at time: {0}".format(env.now))

env = simpy.Environment()
trainStation = TrainStation(env)
env.run()