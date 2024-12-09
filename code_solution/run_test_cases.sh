#!/bin/bash

echo "============================="
echo "Testing Solver"
echo "============================="

counter=0

# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory
for file in test_cases/*
do

  echo "Test case:" "$file"
  timeout 5 python3 minGraphColorSolver.py "$file" outputs/solver-"$counter".txt
  echo

  # https://stackoverflow.com/questions/6348902/how-can-i-add-numbers-in-a-bash-script
  counter=$(($counter+1))

done

echo


echo "============================="
echo "Testing Greedy"
echo "============================="

counter=0

for file in test_cases/*
do

  echo "Test case:" "$file"
  timeout 5 python3 minGraphColorGreedy.py "$file" outputs/greedy-"$counter".txt
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

  echo "Test case:" "$file"
  timeout 5 python3 minGraphColorAnnealing.py "$file" outputs/annealing-"$counter".txt
  echo

  counter=$(($counter+1))

done

echo
