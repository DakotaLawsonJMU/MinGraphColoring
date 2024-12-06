# Idea for a solver
#
# def minColor (Graph):
#     if Graph.verts == 1:
#         return 1
#
#     for n in range(Graph.size - 1):
#        Is this graph colorable (The first two colors are free)

import sys


def createGraph(edges):
    graph = {}

    for v1, v2 in edges:

        if v1 not in graph:
            graph[v1] = {"color": -1, "neighbors": []}
        if v2 not in graph:
            graph[v2] = {"color": -1, "neighbors": []}

        graph[v1]["neighbors"].append(v2)
        graph[v2]["neighbors"].append(v1)

    return graph

def is_n_colorable(graph, n):
    # Helper function to check if a color assignment is valid
    def is_valid_color(vertex, color, graph):
        for neighbor in graph[vertex]["neighbors"]:
            if graph[neighbor]["color"] == color:
                return False
        return True

    # Recursive backtracking function
    def backtrack(vertex_list, index):
        if index == len(vertex_list):  # All vertices have been colored
            return True

        vertex = vertex_list[index]
        for color in range(n):
            if is_valid_color(vertex, color, graph):
                graph[vertex]["color"] = color  # Assign color
                if backtrack(vertex_list, index + 1):  # Recur for the next vertex
                    return True
                graph[vertex]["color"] = -1  # Backtrack (reset color)

        return False  # No valid color found

    # Get the list of vertices
    vertex_list = list(graph.keys())

    # Initialize all vertices to no color (-1)
    for vertex in vertex_list:
        graph[vertex]["color"] = -1

    # Start the backtracking process
    return backtrack(vertex_list, 0)



# Main solution loop
def minColor(graph):
    # Trivial case
    if len(graph) <= 2:
        return len(graph)

    for n in range(2, len(graph) - 1):
        if is_n_colorable(graph, n):
            return n

    return len(graph)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} [input file]")
        exit()

    with open(sys.argv[1]) as file:
        lines = file.read().splitlines()

    num_edges = int(lines.pop(0))
    edges = []

    for line in lines:
        vertices = line.split()
        edges.append((vertices[0], vertices[1]))

    graph = createGraph(edges)

    colors_required = minColor(graph)

    print(colors_required)

    for vertex in graph:
        print(f"{vertex} {graph[vertex]['color']}")


if __name__ == "__main__":
    main()
