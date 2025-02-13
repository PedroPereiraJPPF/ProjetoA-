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
    print(connections_vertices)

########## ALGORITMO A* ##########

index_inicial = 0
index_final = 4
open_list = [{
    'index': index_inicial,
    'f': 0, # f = g + h
    'g': 0, # custo do nó inicial até ele
    'h': 0, # heuristica
    "parent": None
}]
close_list = []

stop = False
while stop != True:
    stop = True

    for item in open_list:
        print(item)
    exit()



# print(vertices)
# print(connections)