#!/bin/bash

python3 random_graph_generator.py test_cases/4-2.txt 4 2
echo "created 4-2.txt"
python3 random_graph_generator.py test_cases/4-3.txt 4 3
echo "created 4-3.txt"

for i in {2..7}; do
  v=$(($i*4))
  sparse=$i
  medium=$(($i*2))
  dense=$(($i*3))

  python3 random_graph_generator.py test_cases/"$v"-"$sparse".txt "$v" "$sparse"
  echo "created" "$v"-"$sparse".txt
  python3 random_graph_generator.py test_cases/"$v"-"$medium".txt "$v" "$medium"
  echo "created" "$v"-"$medium".txt
  python3 random_graph_generator.py test_cases/"$v"-"$dense".txt "$v" "$dense"
  echo "created" "$v"-"$dense".txt
done
