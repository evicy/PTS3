import asynctest
from initialize_nodes import *
import threading
from functions import *

class SystemTest(asynctest.TestCase):
    def setUp(self):
        self.HOST = "localhost"
        graph_base = 8030
        self.graph = {(0,1), (0,2), (2,3), (2,4), (2,7), (4,5), (3,7), (7,8)}
        self.graph = {(graph_base + x, graph_base + y) for x, y in self.graph}
        self.nodes = {x for y in self.graph for x in y}

        self.condition_ready = threading.Condition()
        self.condition_done = threading.Condition()

        self.main_thread = threading.Thread(target=do_stuff,
                    args=[self.HOST, self.nodes, self.graph, self.condition_ready, self.condition_done])
        self.main_thread.start()


    async def test_functions(self):
        with self.condition_ready:
            self.condition_ready.wait()

        self.assertEqual(await climb_degree(8035, HOST=self.HOST), 8032)
        self.assertEqual(await distance4(8035, HOST=self.HOST), {8031, 8038})
        await complete_neighbourhood(8030, HOST=self.HOST)

        #skontrolujeme, ci sedia hrany pomocou get_list_of_neighbours coroutiny
        requester = Requester()
        tasks = [asyncio.create_task(requester.get_list_of_neighbours(node, HOST=self.HOST))
                 for node in [8030, 8031, 8032, 8033, 8034, 8035, 8037, 8038]]
        tasks_results = await asyncio.gather(*tasks)
        for l in tasks_results:
            sorted(l)
        self.assertEqual(tasks_results,
                [[8031, 8032], [8030, 8032], [8030, 8034, 8031, 8037, 8033],
                [8037, 8032], [8035, 8032], [8034], [8038, 8033, 8032], [8037]])

        with self.condition_done:
            self.condition_done.notify()

        self.main_thread.join()
        print("END\n")


if __name__ == '__main__':
    asynctest.main()
