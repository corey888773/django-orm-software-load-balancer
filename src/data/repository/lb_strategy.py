import random
from .abstractions import LoadBalancingStrategyInterface

class RoundRobinStrategy(LoadBalancingStrategyInterface):
    def __init__(self):
        self.index = 0

    def choose(self, servers: list) -> any:
        server = servers[self.index]
        self.index = (self.index + 1) % len(servers)
        return server


class RandomStrategy(LoadBalancingStrategyInterface):
    def choose(self, servers: list) -> any:
        index = random.randint(0, len(servers) - 1)
        server = servers[index]
        return server
