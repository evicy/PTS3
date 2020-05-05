import requests
import asyncio

class Requester:
    async def get_list_of_neighbours(self, start,  HOST="localhost"):
        try:
            r = requests.get(f'http://{HOST}:{start}/')
            neighbours = r.text.split(',')
            neighbours = list(map(int, neighbours))
            return neighbours
        except:
            return []

    async def add_edge(self, e_from, e_to, HOST="localhost"):
       r = requests.get(f'http://{HOST}:{e_from}/new?port={e_to}')
       print("adding edge from ", e_from, "  to ", e_to)


async def complete_neighbourhood(start, HOST="localhost", requester=Requester()):
   print("complete_neighbourhood, start node = ", start)
   neighbours = await requester.get_list_of_neighbours(start, HOST)

   neighbours.append(start)
   print(neighbours)

   tasks = []
   for x in neighbours:
       for y in neighbours:
          if x != y:
               tasks.append(asyncio.create_task(requester.add_edge(x,y, HOST)))

   await asyncio.gather(*tasks)
   print("complete_neighbourhood ready")


async def climb_degree(start, HOST="localhost", requester=Requester()):
    print("climb_degree, start node = ", start)
    neighbours = await requester.get_list_of_neighbours(start, HOST)
    max_degree = len(neighbours)
    if max_degree == 0:
        return start

    port_with_max_degree = start

    async def get_degrees(node):
        node_neighbours = await requester.get_list_of_neighbours(node, HOST)
        return len(node_neighbours)

    tasks = [asyncio.create_task(get_degrees(node)) for node in neighbours]
    tasks_results = await asyncio.gather(*tasks)
    print("tasks_result = ", tasks_results)

    for i in range(len(tasks_results)):
        if (tasks_results[i] > max_degree) or (tasks_results[i] == max_degree and port_with_max_degree > neighbours[i]):
            max_degree = tasks_results[i]
            port_with_max_degree = neighbours[i]

    if start != port_with_max_degree:
        return await climb_degree(port_with_max_degree)

    return port_with_max_degree


async def distance4(start, HOST="localhost", requester=Requester()):
    actual_nodes = set()
    actual_nodes.add(start)
    visited_nodes = set()
    visited_nodes.add(start)

    for i in range(4):
        visited_nodes.update(actual_nodes)

        tasks = [asyncio.create_task(requester.get_list_of_neighbours(node, HOST)) for node in actual_nodes]
        tasks_results = await asyncio.gather(*tasks)

        new_neighbours = set()
        for l in tasks_results:
            new_neighbours.update(l)

        for n in visited_nodes:
            if n in new_neighbours:
                new_neighbours.remove(n)
        actual_nodes = new_neighbours

    return actual_nodes
