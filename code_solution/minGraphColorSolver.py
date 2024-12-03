# Idea for a solver
# 
# def minColor (Graph):
#     if Graph.verts == 1:
#         return 1
#  
#     for n in range(Graph.size - 1):
#        Is this graph colorable (The first two colors are free)

import sys


def createGraph( edges ):
  return []


def minColor( graph ):
  pass


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
    edges.append( (vertices[0], vertices[1]) )

  graph = createGraph( edges )

  colors_required = minColor( graph )

  print(colors_required)

  for vertex in graph:
    print(f"{vertex} {graph[vertex]['color']}")


if __name__ == "__main__":
  main()
