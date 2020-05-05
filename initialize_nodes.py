from http.server  import BaseHTTPRequestHandler, HTTPServer
from node import get_handler
from threading import Thread
import time
import requests
from functions import *
import asyncio

#The condition argument is for you to know when everithing is running
async def do_stuff(HOST, nodes, edges, condition_ready=None, condition_done=None):
    servers = list(HTTPServer((HOST, port), get_handler()) for port in nodes)

    try:   
        threads = list(Thread(target=server.serve_forever) for server in servers)
        for t in threads: t.start()

        def add(x,y):
            r = requests.get(f'http://{HOST}:{x}/new?port={y}')
            r = requests.get(f'http://{HOST}:{y}/new?port={x}')

        for x,y in edges:
            add(x,y)
            add(y, x)

        #complete_neighbourhood(8031, HOST)
        #print("port with highest degree:", climb_degree(8030,HOST))
        #result = set()
        #visited = set()
        #distance4(8030, result, visited)
        #print(result.difference(visited))

        x = await complete_neighbourhood(8030)
        print(x)

        max_port = await climb_degree(8030)
        print(max_port)

        result = await distance4(8030)
        print(result)

        #This is here for you so you know when stuff is ready
        if condition_ready is not None:
            with condition_ready:
                condition_ready.notify()
        
        if condition_done:
            with condition_done:
                condition_done.wait()
        else:
            while True:
                time.sleep(0.5)

    except KeyboardInterrupt:
        pass

    for server in servers:
        server.shutdown()
        server.server_close()
    for t in threads: t.join()


async def main():
    HOST = "localhost"
    graph_base = 8030
    graph = {(0,1), (1, 2), (1, 3), (1, 4), (3, 4), (4, 5)}

    # just a shorter example
    graph = {(0,1), (1,2), (5,4)}

    #for climb_degree
    #graph = {(0,4), (0,2), (2,0), (2,1), (2,3), (4,0), (4,1), (4,3), (3,0), (3,1), (3,2), (3,4)}

    #for distance4
    #graph = {(0,1), (1,2), (2,3), (3,4), (3,5), (2,6), (6,7), (6,8), (4,8), (1,9), (9,10), (10,11), (10,12), (0,11)}

    graph = {(graph_base+x, graph_base+y) for x,y in graph}
    nodes = {x for y in graph for x in y}
    await do_stuff(HOST, nodes, graph)
    print("haloo")
    #x = await complete_neighbourhood(8030)
    #print(x)


if __name__ == "__main__":
    asyncio.run(main())

