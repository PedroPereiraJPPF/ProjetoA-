import pydot
import networkx as nx

# Colocar os dots gerados nesse site https://viz-js.com/

def read_graph_file(filename):
    """ Lê um arquivo DOT e retorna um objeto Graphviz """
    with open(filename, 'r') as file:
        dot_content = file.read()
    graphs = pydot.graph_from_dot_data(dot_content)
    return graphs[0] if graphs else None

def save_graph_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

def parse_graph(dot_content):
    """Converte uma string DOT em um grafo NetworkX."""
    graph = nx.Graph()
    dot_data = pydot.graph_from_dot_data(dot_content)[0]

    for edge in dot_data.get_edges():
        src, dst = edge.get_source(), edge.get_destination()
        weight = edge.get('weight') or 1
        graph.add_edge(src, dst, weight=float(weight))

    return graph

def a_star_search(graph, start, goal):
    """Executa A* para encontrar o caminho mais curto."""
    try:
        path = nx.astar_path(graph, start, goal, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def generate_dot_path(original_dot, path):
    """Gera um novo DOT destacando o caminho encontrado."""
    new_graph = pydot.graph_from_dot_data(original_dot)[0]

    for i in range(len(path) - 1):
        for edge in new_graph.get_edges():
            if (edge.get_source() == path[i] and edge.get_destination() == path[i+1]) or \
               (edge.get_source() == path[i+1] and edge.get_destination() == path[i]):
                edge.set_color("blue")
                edge.set_penwidth(2)

    return new_graph.to_string()

dot_content = read_graph_file("./in/graph.txt").to_string()
graph = parse_graph(dot_content)
path = a_star_search(graph, "A", "D")

if path:
    print("Caminho encontrado:", path)
    new_dot = generate_dot_path(dot_content, path)
    print("\nNovo DOT com caminho traçado:\n", new_dot)

    save_graph_file(new_dot, "./out/pathFile.txt")
else:
    print("Nenhum caminho encontrado.")
