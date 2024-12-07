def summary( file_in, file_out, vertices, edges, colors, nanoseconds ):
  print(f"time:\t\t{round(nanoseconds / 1_000_000_000, 3)}")
  print(f"input file:\t{file_in}")
  print(f"output file:\t{file_out}")
  print(f"vertices:\t{vertices}")
  print(f"edges:\t\t{edges}")
  print(f"colors used:\t{colors}")


def create_graph( edges ):
  
  graph = {}

  for v1, v2 in edges:

    if v1 not in graph:
      graph[v1] = {"color": -1, "neighbors": []}
    if v2 not in graph:
      graph[v2] = {"color": -1, "neighbors": []}

    graph[v1]["neighbors"].append(v2)
    graph[v2]["neighbors"].append(v1)

  return graph

