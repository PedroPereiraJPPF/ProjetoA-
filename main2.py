import pydot
import networkx as nx

def read_graph_file(filename):
    """ Lê um arquivo DOT e retorna um objeto Graphviz """
    with open(filename, 'r') as file:
        dot_content = file.read()
    graphs = pydot.graph_from_dot_data(dot_content)
    return graphs[0] if graphs else None

def save_graph_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

dot_content = read_graph_file("./in/graph.txt").to_string()

words = dot_content.split()

if words[0] != 'graph':
    print("Entrada inválida. Primeira palavra deve ser 'graph'.")
    exit()

graph_Name = words[1]

if words[2] != '{':
    print("Entrada inválida. Terceira palavra deve ser '{'.")
    exit()

if words[3] == '':
    print("Entrada inválida. O grafo deve ter, pelo menos, uma conexão.")
    exit()

connections = []
index = 3
while words[index] != '}':
    if words[index + 1] != '--':
        print("Entrada inválida. Deve haver '--' entre as conexões.")
        exit()

    vertexA = words[index]
    vertexB = words[index + 2]
    
    hasWeight = True 
    weight = 1

    if vertexB[-1] == ';': # caso tenha encerrado é porque não tem peso personalizado
        connections.append((vertexA, vertexB[:-1], 1)) # vertice a, vertice b, peso
    else:
        weight_str = words[index + 3]

        if weight_str.startswith('[weight=') and weight_str.endswith('];'):
            weight = int(weight_str[len('[weight='):-2])
        else:
            print("Entrada inválida. O formato do peso deve ser '[weight=value]'.")
            exit()

        connections.append((vertexA, vertexB, weight))
        index += 1

    index += 3

vertices = []
for connection in connections:
    if connection[0] not in vertices:
        vertices.append(connection[0])
    if connection[1] not in vertices:
        vertices.append(connection[1])

for index in range(len(vertices)):
    for j in range(len(connections)):
        if connections[j][0] == vertices[index]:
            connections[j] = (index, connections[j][1], connections[j][2])
        if connections[j][1] == vertices[index]:
            connections[j] = (connections[j][0], index, connections[j][2])

for index in range(len(vertices)):
    connections_vertices = []

    for connection in connections:
        if connection[0] == index:
            connections_vertices.append(connection)

########## ALGORITMO A* ##########

def define_graph(vertices, connections):
    graph = {}
    current_connections_list = connections.copy()
    current_vertice_list = vertices.copy()

    while current_vertice_list:
        if current_connections_list == []:
            return graph
        
        current_vertice_index = current_connections_list[0][0]
        graph[current_vertice_list[current_vertice_index]] = []

        while len(current_connections_list) > 0 and current_vertice_index == current_connections_list[0][0]:
            graph[current_vertice_list[current_vertice_index]].append(current_connections_list[0])
            current_connections_list.pop(0)
        
    return graph

def get_neighbors(graph, vertices, vertice_name):
    if vertice_name not in vertices:
        return []

    vertice_connections = graph[vertice_name]

    neighbors = []

    if not vertice_connections:
        print("Vertice não encontrado.")
        exit()

    for connection in vertice_connections:
        if connection[1] < 0:
            continue

        neighbor_name = vertices[connection[1]]
        weight = connection[2]

        neighbors.append({"name" : neighbor_name, "weight" : weight})

    return neighbors

def build_path(goal_node):
    path = []
    current_node = goal_node

    while current_node:
        path.append(current_node['index'])
        current_node = current_node['parent']
    
    return path[::-1]
    

def a_star_search(vertices, connections, start, goal):
    """ Usando os vertices e conexões, executa A* para encontrar o caminho mais curto."""

    open_list = [{
        'index': vertices[start],
        'f': 0, # f = g + h
        'g': 0, # custo do nó inicial até ele
        'h': 0, # heuristica
        "parent": None,
        "weight": 0
    }]
    close_list = []

    graph = define_graph(vertices, connections)

    while open_list:
        current_node_index = min(range(len(open_list)), key=lambda i: open_list[i]['weight'])
        current_node = open_list[current_node_index]

        if current_node['index'] == vertices[goal]:
            return build_path(current_node)

        open_list.pop(current_node_index)
        close_list.append(current_node)

        neighbors = get_neighbors(graph, vertices, current_node['index'])

        for neighbor in neighbors:
            if any(node['index'] == neighbor['name'] for node in close_list):
                continue
                
            g = current_node['g'] + neighbor['weight']
            h = heuristic()
            f = g + h

            neighbor_node = {
                'index': neighbor['name'],
                'f': f,
                'g': g,
                'h': h,
                'parent': current_node,
                'weight': neighbor['weight']
            }

            open_list.append(neighbor_node)

    return "Caminho não encontrado."

def heuristic():
    return 0

print(a_star_search(vertices, connections, 0, 2))

# print(vertices)
# print(connections)