# Simulated Annealing approximation of a solution
# to the minimum vertex coloring problem

# https://www.cs.cmu.edu/afs/cs.cmu.edu/project/learn-43/lib/photoz/.g/web/glossary/anneal.html
# https://www.grad.hr/nastava/gs/prg/NumericalRecipesinC.pdf

import sys
import helpers
import time
from enum import Enum
from collections import deque
import random
import math
import minGraphColorGreedy


class ColorMethod(Enum):
    # Have the number of color options be the number of vertices
    # Remove impossible color options, then randomly select remaining
    RANDOM = 1

    # Limit the color options to colors that have already been used
    # Remove impossible color options, then randomly select remaining
    # If no color option remians, add a new color
    ADD_WHEN_NEEDED = 2

    # Use greedy approximation as a starting point
    GREEDY = 3


class Move(Enum):
    # Change the color
    CHANGE = 1

    # Swap the color with another node
    SWAP = 2


def intialize_coloring(graph: dict, method):
    match method:
        case ColorMethod.RANDOM:
            q = deque()

            visited = dict(zip(graph.keys(), [False] * len(graph.keys())))

            start = list(graph.keys())[0]

            visited[start] = True
            q.append(start)

            s = set()
            s.update(range(len(graph.keys())))

            while q:
                next_node_key = q.popleft()
                next_node = graph[next_node_key]
                s_temp = s.copy()

                for neighbor_key in next_node["neighbors"]:
                    neighbor = graph[neighbor_key]
                    s_temp.discard(neighbor["color"])
                    if not visited[neighbor_key]:
                        visited[neighbor_key] = True
                        q.append(neighbor_key)

                next_node["color"] = random.choice(tuple(s_temp))

        case ColorMethod.ADD_WHEN_NEEDED:
            q = deque()

            visited = dict(zip(graph.keys(), [False] * len(graph.keys())))

            start = list(graph.keys())[0]

            visited[start] = True
            q.append(start)

            s = set()

            while q:
                next_node_key = q.popleft()
                next_node = graph[next_node_key]
                s_temp = s.copy()

                for neighbor_key in next_node["neighbors"]:
                    neighbor = graph[neighbor_key]
                    s_temp.discard(neighbor["color"])
                    if not visited[neighbor_key]:
                        visited[neighbor_key] = True
                        q.append(neighbor_key)

                if (len(s_temp) != 0):
                    next_node["color"] = random.choice(tuple(s_temp))

                else:
                    next_node["color"] = len(s)
                    s.add(len(s))

        case ColorMethod.GREEDY:
            colors = []
            start = minGraphColorGreedy.highest_degree_vertex(graph)
            minGraphColorGreedy.color_vertex(start, graph, colors)
            while not minGraphColorGreedy.colored(graph):
                vertex = minGraphColorGreedy.highest_uncolored_degree(graph)
                minGraphColorGreedy.color_neighbors_of([vertex], graph, colors)


def move(graph, temperature, max_temp, node_key,
         colors: set, current_colors: set, method):
    match method:
        case Move.CHANGE:
            added_color = False
            colors_temp = current_colors.copy()
            colors_temp.discard(graph[node_key]["color"])
            for neighbor_key in graph[node_key]["neighbors"]:
                neighbor = graph[neighbor_key]
                colors_temp.discard(neighbor["color"])
            new_color = -1
            if len(colors_temp) != 0:
                new_color = random.choice(tuple(colors_temp))
            else:
                new_color = max(colors.keys()) + 1
                added_color = True

            value = value_change(graph, temperature, max_temp, node_key,
                                 colors, current_colors,
                                 new_color, added_color)

            if random.random() <= value:
                if colors[graph[node_key]["color"]] == 1:
                    colors[graph[node_key]["color"]] -= 1
                    current_colors.remove(graph[node_key]["color"])
                    if added_color:
                        colors[new_color] = 1
                        current_colors.add(new_color)
                    else:
                        colors[new_color] += 1
                else:
                    colors[graph[node_key]["color"]] -= 1
                    if added_color:
                        colors[new_color] = 1
                        current_colors.add(new_color)
                    else:
                        colors[new_color] += 1
                graph[node_key]["color"] = new_color

        case Move.SWAP:
            pass


def deviation(colors, current_colors):
    processed_dict = dict()
    for key in current_colors:
        processed_dict[key] = colors[key]
    amounts = list(processed_dict.values())
    avg = sum(amounts) / len(amounts)
    sum_diff = 0
    for amount in amounts:
        sum_diff += ((amount - avg) ** 2)
    std_deviation = math.sqrt(sum_diff / len(amounts))
    return std_deviation


def get_local_dist(graph, node_key, depth):
    visited = set()
    queue = deque()
    queue.append((node_key, 0))
    colors = dict()

    while len(queue) > 0:
        curr_tuple = queue.popleft()
        curr_node = curr_tuple[0]
        curr_depth = curr_tuple[1]
        if curr_node in visited or curr_depth > depth:
            continue

        visited.add(curr_node)
        if graph[curr_node]['color'] in colors.keys():
            colors[graph[curr_node]['color']] += 1
        else:
            colors[graph[curr_node]['color']] = 1

        if curr_depth < depth:
            for neighbor_key in graph[curr_node]['neighbors']:
                if neighbor_key not in visited:
                    queue.append((neighbor_key, curr_depth + 1))

    current_colors = set(colors.keys())
    return (colors, current_colors)


def change_dist(graph, node_key, colors,
                current_colors, new_color, added_color):
    colors_temp = colors.copy()
    current_colors_temp = current_colors.copy()
    if colors[graph[node_key]["color"]] == 1:
        colors_temp[graph[node_key]["color"]] -= 1
        current_colors_temp.remove(graph[node_key]["color"])
        if added_color:
            colors_temp[new_color] = 1
        else:
            colors_temp[new_color] += 1
    else:
        colors_temp[graph[node_key]["color"]] -= 1
        if added_color:
            colors_temp[new_color] = 1
        else:
            colors_temp[new_color] += 1
    return (colors_temp, current_colors_temp)


def value_change(graph, temperature, max_temp, node_key,
                 colors: dict, current_colors, new_color, added_color):
    num_colors = 0.6
    all_proportion = 0.1
    local_proportion = 0.2

    local_depth = 2

    chance = 0.1 * (temperature / max_temp)

    if not added_color and colors[graph[node_key]["color"]] == 1:
        chance += num_colors

    colors_temp, current_colors_temp = change_dist(graph,
                                                   node_key,
                                                   colors,
                                                   current_colors,
                                                   new_color,
                                                   added_color)

    curr_deviation = deviation(colors, current_colors)
    change_deviation = deviation(colors_temp, current_colors_temp)

    if change_deviation < curr_deviation:
        chance += all_proportion

    local_colors, local_current_colors = get_local_dist(graph,
                                                        node_key, local_depth)
    local_colors_temp, local_current_colors_temp = change_dist(
        graph, node_key, colors, local_current_colors, new_color, added_color)

    curr_local_deviation = deviation(local_colors, local_current_colors)
    change_local_devation = deviation(local_colors_temp,
                                      local_current_colors_temp)

    if change_local_devation < curr_local_deviation:
        chance += local_proportion

    return chance


def validate_graph(graph: dict):
    q = deque()

    visited = dict(zip(graph.keys(), [False] * len(graph.keys())))

    start = list(graph.keys())[0]

    visited[start] = True
    q.append(start)

    s = dict()

    while q:
        next_node_key = q.popleft()
        next_node = graph[next_node_key]
        if (next_node["color"] == -1):
            return -1

        if (next_node["color"] in s.keys()):
            s[next_node["color"]] += 1
        else:
            s[next_node["color"]] = 1

        for neighbor_key in next_node["neighbors"]:
            neighbor = graph[neighbor_key]
            if neighbor["color"] == next_node["color"]:
                return -1

            if not visited[neighbor_key]:
                visited[neighbor_key] = True
                q.append(neighbor_key)

    return s


def annealing_approx(graph: dict):
    # The value of a graph should increase if:
    #   - the number of colors decreases
    #   - the proportion of numbers becomes more even
    #   - the distribution of colors becomes more even
    # The distribution of colors can be simplified to local proportions
    # The size of the local region is dependent upon how many ancestor
    # neighbors are visited (i.e. depth of 1, 2 etc.)
    # The global proportion may or may not be needed, I'm not sure if
    # only using local proportions will cause regional isolations of
    # maximized graphs that don't mesh with each other and result in
    # greater overall colors.
    intialize_coloring(graph, ColorMethod.ADD_WHEN_NEEDED)
    max_temp = len(graph.keys())
    tempurature = max_temp

    colors = validate_graph(graph)
    current_colors = set(colors.keys())
    s = set()
    s.update(graph.keys())

    while tempurature > 0:
        s_temp = s.copy()
        random_node_key = random.choice(tuple(s_temp))
        move(graph, tempurature, max_temp,
             random_node_key, colors, current_colors, Move.CHANGE)
        tempurature -= 1

    return len(validate_graph(graph))


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

    graph: dict = helpers.create_graph(edges)

    start = time.time_ns()
    solution = annealing_approx(graph)
    end = time.time_ns()

    helpers.summary(sys.argv[1], sys.argv[2], len(graph),
                    num_edges, solution, end - start)

    with open(sys.argv[2], 'w') as file:
        file.write(f"{solution}\n")

        for vertex in graph:
            file.write(f"{vertex} {graph[vertex]['color']}\n")


if __name__ == "__main__":
    main()
