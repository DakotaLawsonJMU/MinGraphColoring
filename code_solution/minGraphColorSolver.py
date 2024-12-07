# Idea for a solver
#
# def minColor (Graph):
#     if Graph.verts == 1:
#         return 1
#
#     for n in range(Graph.size - 1):
#        Is this graph colorable (The first two colors are free)

import sys
import time
import helpers


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

    if len(graph) > 2:
        for n in range(2, len(graph)):
            if is_n_colorable(graph, n):
                return n

    # if this point is reached, graph is complete, and each vertex gets a unique color
    color = 0
    for vertex in graph:
        graph[vertex]["color"] = color
        color += 1

    return len(graph)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} [input file] [output file]")
        exit()

    with open(sys.argv[1]) as file:
        lines = file.read().splitlines()

    num_edges = int(lines.pop(0))
    edges = []

    for line in lines:
        vertices = line.split()
        edges.append((vertices[0], vertices[1]))

    graph = helpers.create_graph(edges)

    start = time.time_ns()
    colors_required = minColor(graph)
    end = time.time_ns()

    helpers.summary( sys.argv[1], sys.argv[2], len(graph), num_edges, colors_required, end - start )

    with open(sys.argv[2], 'w') as file:
        file.write(f"{colors_required}\n")

        for vertex in graph:
            file.write(f"{vertex} {graph[vertex]['color']}\n")


if __name__ == "__main__":
    main()
