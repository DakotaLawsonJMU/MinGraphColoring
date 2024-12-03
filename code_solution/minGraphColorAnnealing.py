# Simulated Annealing approximation of a solution to the minimum vertex coloring problem

# https://www.cs.cmu.edu/afs/cs.cmu.edu/project/learn-43/lib/photoz/.g/web/glossary/anneal.html
# https://www.grad.hr/nastava/gs/prg/NumericalRecipesinC.pdf

import sys


def create_graph( edges ):
  return []


def annealing_approximation( graph ):
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

  graph = create_graph( edges )

  colors_required = annealing_approximation( graph )

  print(colors_required)

  for vertex in graph:
    print(f"{vertex} {graph[vertex]['color']}")


if __name__ == "__main__":
  main()
