import unittest
from functions import *
from initialize_nodes import *
import asyncio
from asyncio import events


class SystemTest(unittest.TestCase):
    def setUp(self):
        HOST = "localhost"
        graph_base = 8030
        graph = {(0, 1), (1, 2), (1, 3), (1, 4), (3, 4), (4, 5)}
        graph = {(graph_base + x, graph_base + y) for x, y in graph}
        nodes = {x for y in graph for x in y}

        self.condition_ready = asyncio.Condition()
        self.condition_done = asyncio.Condition()

        loop = asyncio.get_event_loop()
        task = loop.create_task(do_stuff(HOST, nodes, graph, self.condition_ready, self.condition_done))

    def test_complete_neighbourhood(self):
        async def complete_neighbourhood_wrapper():
            async with self.condition_ready:
                await self.condition_ready.wait()
                await complete_neighbourhood(8030)
                self.condition_done.notify()
        loop = asyncio.get_event_loop()
        task = loop.create_task(complete_neighbourhood_wrapper())
        loop.run_forever()
        print("END\n")


if __name__ == '__main__':
    unittest.main()
