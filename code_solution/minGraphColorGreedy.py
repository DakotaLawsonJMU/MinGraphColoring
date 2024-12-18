import sys
import time
import helpers

def color_vertex( vertex, graph, colors ):

  colors_copy = colors.copy()

  for neighbor in graph[vertex]["neighbors"]:
    color = graph[neighbor]["color"]
    if color > -1 and color in colors_copy:
      colors_copy.remove(color)

  if len(colors_copy) == 0:
    graph[vertex]["color"] = len(colors)
    colors.append(len(colors))
  else:
    graph[vertex]["color"] = colors_copy[0]
  


def local_graph( vertices, graph ):
  local = []

  for vertex in graph:

    if graph[vertex]["color"] != -1:
      continue

    in_local = True

    for required_neighbor in vertices:
      if required_neighbor not in graph[vertex]["neighbors"]:
        in_local = False
        break

    if in_local:
      local.append(vertex)

  return local


def color_neighbors_of( vertices, graph, colors ):

  # list of all vertices adjacent to everything in given vertices list
  local = local_graph( vertices, graph )
  #print(f"locality: {local}")

  while len(local) != 0:
    next_vertex = highest_local_uncolored_degree( graph, local )
    color_vertex( next_vertex, graph, colors )

    vertices.append( next_vertex )
    color_neighbors_of( vertices, graph, colors )
    vertices.pop()

    local = local_graph( vertices, graph )


def highest_degree_vertex( graph ):
  highest_degree = -1
  retval = None

  for vertex in graph:
    if len(graph[vertex]["neighbors"]) > highest_degree:
      highest_degree = len(graph[vertex]["neighbors"])
      retval = vertex

  return retval


# returns the colored vertex with the highest uncolored degree
def highest_uncolored_degree( graph ):
  highest_degree = -1
  retval = None

  for vertex in graph:
    degree = 0

    if graph[vertex]["color"] == -1:
      continue

    for neighbor in graph[vertex]["neighbors"]:
      if graph[neighbor]["color"] == -1:
        degree += 1

    if degree > highest_degree:
      highest_degree = degree 
      retval = vertex

  return retval


# return the uncolored vertex in the locality with the most adjacent
# uncolored neighbors also in the locality
def highest_local_uncolored_degree( graph, locality ):
  highest_degree = -1
  retval = None

  for vertex in locality:
    degree = 0

    for neighbor in graph[vertex]["neighbors"]:
      if neighbor in locality:
        degree += 1

    if degree > highest_degree:
      highest_degree = degree
      retval = vertex
  
  return retval


def colored( graph ):
  for vertex in graph:
    if graph[vertex]["color"] == -1:
      return False
  return True


# Greedy approximation of a solution to the minimum vertex coloring problem

# Pick the highest degree vertex v in the graph and color it
# Pick the vertex v' adjacent to v with the most uncolored neighbors also adjacent to v
# color it
# Pick the vertex v'' adjacent to v and v' with the most uncolored neighbors also adjacent to v and v'
# color it
# continue until there are no vertices adjacent to v, v', v'', v''' ...
# return to the last sequence of vertices that does have 1+ adjacent vertices and color them
# once v and all its neighbors are colored, start with a new v
# the new v must be adjacent to a colored vertex and have the most uncolored neighbors
# color it and repeat recursive sequence
def min_color_approx( graph ):
  colors = []

  # Start at the highest degree vertex and color it
  start = highest_degree_vertex( graph )
  color_vertex( start, graph, colors )

  # while the coloring is not done choose the colored vertex adjacent
  # to the most uncolored vertices, and color those uncolored neighbors
  while not colored( graph ):
    vertex = highest_uncolored_degree( graph )
    color_neighbors_of( [vertex], graph, colors )

  return len(colors)

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
    edges.append( (vertices[0], vertices[1]) )

  graph = helpers.create_graph( edges )

  start = time.time_ns()
  solution = min_color_approx( graph )
  end = time.time_ns()

  helpers.summary( sys.argv[1], sys.argv[2], len(graph), num_edges, solution, end - start )

  with open(sys.argv[2], 'w') as file:
    file.write(f"{solution}\n")

    for vertex in graph:
      file.write(f"{vertex} {graph[vertex]['color']}\n")
      

if __name__ == "__main__":
  main()
