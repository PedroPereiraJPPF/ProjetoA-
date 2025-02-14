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

def ItemIsOnList(list, item_index):
    for item in list:
        if item['index'] == item_index:
            return True
    return False

def finalizar(close_list, index_start, index_end):
    path_graph = []

    while index_end != None:
        for item in close_list:
            if item['index'] == index_end:
                path_graph.append(vertices[item['index']])
                index_end = item["parent"]
                break

    path_graph = list(reversed(path_graph))
    print(path_graph)

    exit()

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

connections_vertices = []
for index in range(len(vertices)):
    vertex_connections = []

    for connection in connections:
        if connection[0] == index:
            vertex_connections.append(connection)
        if connection[1] == index:
            vertex_connections.append(connection)

    connections_vertices.append(vertex_connections)

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

etapa = 0
while True:
    etapa += 1

    index_melhor = 0
    custo_melhor = open_list[0]['g']
    count = 0
    for item in open_list:
        if item['g'] < custo_melhor:
            custo_melhor = item['g'] # trocar para heuristica depois
            index_melhor = count
        count += 1

    item = open_list.pop(index_melhor)
    close_list.append(item)

    index_item = item['index']
    item_connections = connections_vertices[index_item]

    if item['index'] == index_final:
        finalizar(close_list, index_inicial, index_final)
    
    for connection in item_connections:
        item_destiny = connection[1]

        if item_destiny == index_item:
            item_destiny = connection[0]

        isOnCloseList = ItemIsOnList(close_list, item_destiny)

        if isOnCloseList == False:
            destiny_value = connection[1]
            if connection[0] != index_item:
                destiny_value = connection[0]
            weight = connection[2]

            # Checa se o valor de destino já foi testado
            checked = False
            for item_open in close_list:
                if item_open['index'] == destiny_value:
                    checked = True
                    break

            is_opened = ItemIsOnList(open_list, destiny_value)

            if is_opened == True:
                new_weight = weight + item_open['g']

                for i in range(len(open_list)):
                    if destiny_value == open_list[i]['index']:
                        if open_list[i]['g'] > new_weight:
                            open_list[i] = {
                                'index': destiny_value,
                                'f': 0,
                                'g': new_weight,
                                'h': 0,
                                'parent': index_item
                            }

            else:
                is_closed = ItemIsOnList(close_list, destiny_value)
                
                if is_closed == False:
                    open_list.append({
                        'index': destiny_value,
                        'f': 0, # mudar para peso + heuristica
                        'g': weight + item_open['g'],
                        'h': 0,
                        'parent': index_item
                    })

#print(vertices)
#print(connections)