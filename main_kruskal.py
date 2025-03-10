import pydot
import networkx as nx
import GraphRender

path_graph = []

def read_graph_file(filename):
    """ Lê um arquivo DOT e retorna um objeto Graphviz """
    with open(filename, 'r') as file:
        dot_content = file.read()
    graphs = pydot.graph_from_dot_data(dot_content)
    return graphs[0] if graphs else None

def save_graph_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

def generate_dot_path(original_dot, path):
    """Gera um novo DOT destacando o caminho encontrado."""
    new_graph = pydot.graph_from_dot_data(original_dot)[0]
    path = [item for sublist in path for item in sublist]

    for i in range(len(path) - 1):
        for edge in new_graph.get_edges():
            if (edge.get_source() == path[i] and edge.get_destination() == path[i+1]) or \
               (edge.get_source() == path[i+1] and edge.get_destination() == path[i]):
                edge.set_color("blue")
                edge.set_penwidth(5)
                edge.set_label(edge.get('weight'))

    return new_graph.to_string()

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

def checkCicle(connections):
    G = nx.Graph()


    for i in connections:
        G.add_edge(i[0], i[1])

    try:
        cycle = nx.find_cycle(G)
    except nx.NetworkXNoCycle:
        return False

    return True



# Ordenar as arestas em ordem crescente
connections = sorted(connections, key=lambda x: x[2])

num_lines = 0
connections_kruskal = []

# Armazenamento de labels
vertices = []
for connection in connections:
    if connection[0] not in vertices:
        vertices.append(connection[0])
    if connection[1] not in vertices:
        vertices.append(connection[1])

count = 0

while len(connections_kruskal) < len(vertices) - 1:
    G = nx.Graph()
    
    connections_kruskal.append(connections[0])
    connections.pop(0)

    if checkCicle(connections_kruskal):
        connections_kruskal.pop(-1)
    else:
        # tô usando o loop para gerar imagens do caminho
        graph_str = generate_dot_path(dot_content, connections_kruskal)
        graph = pydot.graph_from_dot_data(graph_str)[0]
        
        count += 1
        graph.write_png(f'./out/graph_iteration_{count}_kruskal.png')

        print("Etapa: ", count)

# Aqui o grafo final é exibido
graph_render = GraphRender.GraphRender(image_folder='./out', algorithm='kruskal', screen_name="Kruskal")
graph_render.navigate()