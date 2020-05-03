from http.server  import BaseHTTPRequestHandler, HTTPServer
from node import get_handler
from threading import Thread
import time
import requests

def get_list_of_neighbours(start,  HOST = "localhost"):
    r = requests.get(f'http://{HOST}:{start}/')
    neighbours = r.text.split(',')
    neighbours = list(map(int, neighbours))
    return neighbours

def complete_neighbourhood(start,  HOST = "localhost"):
    neighbours = get_list_of_neighbours(start, HOST)

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


def climb_degree(start, HOST = "localhost"):
    neighbours = get_list_of_neighbours(start, HOST)
    max_degree = len(neighbours)
    if max_degree == 0:
        return start

    port_with_max_degree = start

    degrees = []
    for n in neighbours:
        degrees.append((n, len(get_list_of_neighbours(n, HOST))))

    print(degrees)
    degrees = sorted(degrees, key=lambda element: (element[1] * -1, element[0]))
    print(degrees)

    best_tuple = degrees[0]

    if best_tuple[1] == max_degree:
        return min(best_tuple[0], port_with_max_degree)

    if best_tuple[1] > max_degree:
        return climb_degree(best_tuple[0], HOST)

    return port_with_max_degree


def distance4(start, result, visited_sooner, distance=0):
    visited_sooner.add(start)
    neighbours = get_list_of_neighbours(start, HOST)

    if distance == 3:
        for n in neighbours:
            if n not in visited_sooner:
                result.add(n)

    if distance < 3:
        for n in neighbours:
            distance4(n, result, visited_sooner, distance+1)



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

        #complete_neighbourhood(8031, HOST)
        #print("port with highest degree:", climb_degree(8030,HOST))
        result = set()
        visited = set()
        distance4(8030, result, visited)
        print(result.difference(visited))

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

    # just a shorter example
    #graph = {(0,1), (1,2), (5,4)}

    #for climb_degree
    #graph = {(0,4), (0,2), (2,0), (2,1), (2,3), (4,0), (4,1), (4,3), (3,0), (3,1), (3,2), (3,4)}

    #for distance4
    graph = {(0,1), (1,2), (2,3), (3,4), (3,5), (2,6), (6,7), (6,8), (4,8), (1,9), (9,10), (10,11), (10,12), (0,11)}

    graph = {(graph_base+x, graph_base+y) for x,y in graph}
    nodes = {x for y in graph for x in y}
    do_stuff(HOST, nodes, graph)
    print("haloo")

