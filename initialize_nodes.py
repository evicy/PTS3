from http.server  import BaseHTTPRequestHandler, HTTPServer
from node import get_handler
from threading import Thread
import time
import requests

def complete_neighbourhood(start,  HOST = "localhost"):
    r = requests.get(f'http://{HOST}:{start}/')
    neighbours = r.text.split(',')
    neighbours.append(start)
    print(neighbours)

    def add_edge(e_from, e_to):
        r = requests.get(f'http://{HOST}:{e_from}/new?port={e_to}')

    for x in neighbours:
        for y in neighbours:
            if x != y:
                add_edge(x,y)
                #print("adding from", x, " to ", y)

    print("complete_neighbourhood ready")




#The condition argument is for you to know when everithing is running
def do_stuff(HOST, nodes, edges, condition_ready=None, condition_done=None):
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

        complete_neighbourhood(8031, HOST)

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


if __name__=="__main__":
    HOST = "localhost"
    graph_base = 8030
    graph = {(0,1), (1, 2), (1, 3), (1, 4), (3, 4), (4, 5)}
    graph = {(0,1), (1,2), (5,4)}
    graph = {(graph_base+x, graph_base+y) for x,y in graph}
    nodes = {x for y in graph for x in y}
    do_stuff(HOST, nodes, graph)
    print("haloo")

