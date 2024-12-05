import sys


def main():
  if len(sys.argv) != 3:
    print("This script generates a complete graph of a given size and stores it in a file")
    print(f"Usage: python3 {sys.argv[0]} <output file> <graph size>")
    exit()

  V = int(sys.argv[2])
  E = (V * (V-1)) // 2

  with open(sys.argv[1], 'w') as file:
    file.write(str(E)+"\n")

    for v1 in range(0, V):
      for v2 in range(v1+1, V):
        file.write(f"v{v1} v{v2}\n")


if __name__ == "__main__":
  main()
