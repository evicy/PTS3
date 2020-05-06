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
            #print("mocking get_list_of_neighbours for node", node)
            await asyncio.sleep(5)
            return self.node_neighbours[node].copy()

        self.mock_requester.get_list_of_neighbours = mock_neighbours

        async def mock_add_edge(e_from, e_to, HOST=''):
            if e_to not in self.node_neighbours[e_from]:
                #print("mocking add_edge from = ", e_from, "  to ", e_to)
                self.node_neighbours[e_from].append(e_to)
                await asyncio.sleep(5)

        self.mock_requester.add_edge = mock_add_edge


    # mock_neighbours called 6 times = 30 seconds sequentially
    # 3 mock_neighbours parallel (for nodes 8030, 8032, 8033)
    # 3 mock_neighbours sequential (for nodes 8030, 2*8031)
    def test_climb_degree(self):
        start_time = time.time()
        self.assertEqual(asyncio.run(climb_degree(8030, requester=self.mock_requester)), 8031)
        print("test_climb_degree: -- %s seconds --" % (time.time() - start_time), " expected around 20 seconds\n")
        self.assertTrue(20 <= (time.time() - start_time) < 30)


    # mock_neighbours called 6 times = 30 seconds
    # 2*2 mock_neighbours parallel (for nodes (8032, 8033) and (8034, 8035)) = 2*5sec
    # 2 mock_neighbours sequential (pre vrcholy 8030, 8031) = 2*5sec
    def test_distance4(self):
        start_time = time.time()
        self.assertEqual(asyncio.run(distance4(8030, requester=self.mock_requester)), {8036, 8037})
        print("test_distance4: -- %s seconds --" % (time.time() - start_time), " expected around: 20 seconds\n")
        self.assertTrue(20 <= (time.time() - start_time) < 30)


    # mock_neighbours called once, mock_add_edge called 4times = 25sec sequentially
    # 4 mock_add_edge parallel (from nodes 8036 a 8037)
    # 1 mock_neighbours sequential (for nodes 8034)
    def test_complete_neighbourhood(self):
        start_time = time.time()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(complete_neighbourhood(8034, requester=self.mock_requester))
        loop.close()
        print("test_complete_neighbourhood: -- %s seconds --AA" % (time.time() - start_time), " expected around 10 seconds\n")
        self.assertTrue(10.0 <= (time.time() - start_time) < 25.0)
        self.assertEqual(sorted(self.node_neighbours[8034]), [8036, 8037])
        self.assertEqual(sorted(self.node_neighbours[8036]), [8034, 8037])
        self.assertEqual(sorted(self.node_neighbours[8037]), [8034, 8036])


if __name__ == '__main__':
    unittest.main()
