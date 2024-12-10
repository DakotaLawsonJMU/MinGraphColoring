#!/bin/bash

echo "============================="
echo "Testing Solver"
echo "============================="

counter=0

touch results.txt
truncate -s 0 results.txt

# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory
for file in test_cases/*
do

  echo "Test case:" "$file"

  # https://stackoverflow.com/questions/7851889/kill-process-after-a-given-time-bash
  timeout 3 python3 minGraphColorSolver.py "$file" outputs/solver-"$counter".txt | tee -a results.txt

  echo

  # https://stackoverflow.com/questions/6348902/how-can-i-add-numbers-in-a-bash-script
  counter=$(($counter+1))

done

python3 minGraphColorSolver.py test_cases/k-11.txt outputs/solver-"$counter".txt | tee -a results.txt
python3 minGraphColorSolver.py test_cases/k-12.txt outputs/solver-"$counter".txt | tee -a results.txt
python3 minGraphColorSolver.py test_cases/k-13.txt outputs/solver-"$counter".txt | tee -a results.txt
counter=$(($counter+1))

echo


echo "============================="
echo "Testing Greedy"
echo "============================="

counter=0

for file in test_cases/*
do

  echo "Test case:" "$file"
  timeout 3 python3 minGraphColorGreedy.py "$file" outputs/greedy-"$counter".txt | tee -a results.txt
  echo

  counter=$(($counter+1))

done

echo

echo "============================="
echo "Testing Annealing"
echo "============================="

counter=0

for file in test_cases/*
do

  for i in {0..9}
  do
    echo "Test case:" "$file"
    timeout 3 python3 minGraphColorAnnealing.py "$file" outputs/annealing-"$counter".txt | tee -a results.txt
    echo
    counter=$(($counter+1))
  done


done

echo
