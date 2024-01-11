import random
from .abstractions import LoadBalancingStrategyInterface
from ..database import DatabaseWrapper

class RoundRobinStrategy(LoadBalancingStrategyInterface):
    def __init__(self):
        self.index = 0

    async def choose(self, servers: list[DatabaseWrapper]) -> DatabaseWrapper:
        while True:
            server = servers[self.index]
            self.index = (self.index + 1) % len(servers)

            if await server.is_connected():
                break
            
        return server


class RandomStrategy(LoadBalancingStrategyInterface):
    async def choose(self, servers: list[DatabaseWrapper]) -> DatabaseWrapper:
        while True:
            index = random.randint(0, len(servers) - 1)
            server = servers[index]

            if await server.is_connected():
                break
            else:
                servers.pop(index)

        return server

