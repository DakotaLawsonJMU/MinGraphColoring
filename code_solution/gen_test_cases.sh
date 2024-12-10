#!/bin/bash

#python3 random_graph_generator.py test_cases/4-2.txt 4 2
#echo "created 4-2.txt"
#python3 random_graph_generator.py test_cases/4-3.txt 4 3
#echo "created 4-3.txt"

#for i in {2..7}; do
#  for j in {0..3}; do
#    v=$(($i*4+j))
#    sparse=$(($i))
#    medium=$(($i*2))
#    dense=$(($i*3))
#
#    python3 random_graph_generator.py test_cases/"$v"-"$sparse".txt "$v" "$sparse"
#    echo "created" "$v"-"$sparse".txt
#    python3 random_graph_generator.py test_cases/"$v"-"$medium".txt "$v" "$medium"
#    echo "created" "$v"-"$medium".txt
#    python3 random_graph_generator.py test_cases/"$v"-"$dense".txt "$v" "$dense"
#    echo "created" "$v"-"$dense".txt
#  done
#done

for i in {2..15}; do
  python3 random_graph_generator.py test_cases/21-"$i".txt 21 "$i"
  echo "created 21-$i.txt"
done

for i in {3..16}; do
  python3 complete_graph_generator.py test_cases/k-"$i".txt "$i"
  echo "created k-$i.txt"
done

python3 complete_graph_generator.py test_cases/k-64.txt 64 
echo "created k-64.txt"

python3 complete_graph_generator.py test_cases/k-256.txt 256
echo "created k-256.txt"

python3 complete_graph_generator.py test_cases/k-64.txt 1024
echo "created k-1024.txt"
