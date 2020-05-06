import asynctest
from initialize_nodes import *
import asyncio
import threading
from functions import *
import responses



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
        self.assertEqual(await distance4(8035, HOST=self.HOST), {8038})

        with self.condition_done:
            self.condition_done.notify()

        self.main_thread.join()
        print("END\n")


if __name__ == '__main__':
    asynctest.main()
