import unittest
from unittest.mock import AsyncMock
from functions import *


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.mock_requester = AsyncMock()
        self.node_neighbours = {8030: [8031], 8031: [8030, 8032, 8033],
                                8032: [8031, 8034, 8035], 8033: [8031],
                                8034: [8036, 8037], 8035: [8032], 8036: [], 8037: []}

        async def mock_neighbours(node, HOST=''):
            return self.node_neighbours[node].copy()

        self.mock_requester.get_list_of_neighbours = mock_neighbours

        async def mock_add_edge(e_from, e_to, HOST=''):
            if e_to not in self.node_neighbours[e_from]:
                self.node_neighbours[e_from].append(e_to)

        self.mock_requester.add_edge = mock_add_edge


    def test_climb_degree(self):
        self.assertEqual(asyncio.run(climb_degree(8030, requester=self.mock_requester)), 8031)

    def test_distance4(self):
        self.assertEqual(asyncio.run(distance4(8030, requester=self.mock_requester)), {8036, 8037})

    def test_complete_neighbourhood(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(complete_neighbourhood(8034, requester=self.mock_requester))
        loop.close()
        self.assertEqual(sorted(self.node_neighbours[8034]), [8036, 8037])
        self.assertEqual(sorted(self.node_neighbours[8036]), [8034, 8037])
        self.assertEqual(sorted(self.node_neighbours[8037]), [8034, 8036])


if __name__ == '__main__':
    unittest.main()
