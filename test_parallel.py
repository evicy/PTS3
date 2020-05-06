import unittest
from unittest.mock import AsyncMock
from functions import *
import asyncio
import time


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_requester = AsyncMock()
        self.node_neighbours = {8030: [8031], 8031: [8030, 8032, 8033],
                                8032: [8031, 8034, 8035], 8033: [8031],
                                8034: [8036, 8037], 8035: [8032], 8036: [], 8037: []}

        async def mock_neighbours(node, HOST=''):
            print("mocking get_list_of_neighbours for node", node)
            await asyncio.sleep(5)
            return self.node_neighbours[node].copy()

        self.mock_requester.get_list_of_neighbours = mock_neighbours

        async def mock_add_edge(e_from, e_to, HOST=''):
            #print("mock_add_edge BEGINNING", self.node_neighbours)
            if e_to not in self.node_neighbours[e_from]:
                #print(self.node_neighbours)
                print("mocking add_edge from = ", e_from, "  to ", e_to)
                self.node_neighbours[e_from].append(e_to)
                await asyncio.sleep(5)
                #print(self.node_neighbours, "\n")

        self.mock_requester.add_edge = mock_add_edge

    # 3 mock_neighbours mozu robit paralelne (pre vrcholy 8030, 8032, 8033)
    # 3 mock_neighbours treba pockat (pre vrcholy 8030, 2*8031)
    def test_climb_degree(self):
        start_time = time.time()
        self.assertEqual(asyncio.run(climb_degree(8030, requester=self.mock_requester)), 8031)
        print("test_climb_degree: --- %s seconds ---" % (time.time() - start_time))
        print("test_climb_degree: mock_neighbours called 6times (6*5=30sec sequentially)")
        print("test_climb_degree: expected duration: 3*5 + 1*5 = 20sec\n")

    # 2*2 mock_neighbours mozu robit paralelne (pre vrcholy (8032, 8033) a (8034, 8035))
    # 2 mock_neighbours treba pockat (pre vrcholy 8030, 8031)
    def test_distance4(self):
        start_time = time.time()
        self.assertEqual(asyncio.run(distance4(8030, requester=self.mock_requester)), {8036, 8037})
        print("test_distance4: --- %s seconds ---" % (time.time() - start_time))
        print("test_distance4: mock_neighbours called 6times (6*5=30sec sequentially)")
        print("test_climb_degree: expected duration: 2*5 + 1*5 + 1*5 = 20sec\n")

    # 4 mock_add_edge mozu robit paralelne (z vrcholov 8036 a 8037)
    # 1 mock_neighbours treba pockat (pre vrchol 8034)
    def test_complete_neighbourhood(self):
        start_time = time.time()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(complete_neighbourhood(8034, requester=self.mock_requester))
        loop.close()
        print("test_complete_neighbourhood: --- %s seconds ---" % (time.time() - start_time))
        print("test_complete_neighbourhood: mock_neighbours called once (5sec) ",
              "and 4xparalel mock_add_edge (4*5sec) (= together 25sec sequentially)")
        print("test_complete_neighbourhood: expected duration: 1*5 + 1*5 = 10sec\n")
        self.assertEqual(sorted(self.node_neighbours[8034]), [8036, 8037])
        self.assertEqual(sorted(self.node_neighbours[8036]), [8034, 8037])
        self.assertEqual(sorted(self.node_neighbours[8037]), [8034, 8036])


if __name__ == '__main__':
    unittest.main()
