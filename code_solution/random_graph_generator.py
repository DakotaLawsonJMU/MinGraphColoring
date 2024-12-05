import sys
import random


def main():
  if len(sys.argv) != 4:
    print("This script generates a random graph of a given size and given avg degree and stores it in a file")
    print(f"Usage: python3 {sys.argv[0]} <output file> <vertices> <degree>")
    exit()

  V = int(sys.argv[2])
  E = int(int(sys.argv[3])/2 * V)

  if E < V-1:
    print("input a higher degree")
    exit()

  # all absent edges of the graph except those of the form (v_n, v_n+1)
  absent_edges = []
  for v1 in range(0, V-2):
    for v2 in range(v1+2, V):
      absent_edges.append( (v1, v2) )


  with open(sys.argv[1], 'w') as file:
    file.write(str(E)+"\n")

    for v in range(0, V-1):
      file.write(f"v{v} v{v+1}\n")

    for i in range(V-1, E):
      index = random.randint(0, len(absent_edges)-1)

      (v1, v2) = absent_edges.pop(index)

      file.write(f"v{v1} v{v2}\n")
      

if __name__ == "__main__":
  main()
