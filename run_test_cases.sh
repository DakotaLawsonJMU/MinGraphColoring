#!/bin/bash

# https://stackoverflow.com/questions/10523415/execute-command-on-all-files-in-a-directory
for program in code_solution/*
do

  echo "============================="
  echo "Testing" "$program"
  echo "=============================\n"

  for file in test_cases/*
  do

    echo "Test case:" "$file"
    python3 "$program" "$file"
    echo

  done

  echo

done

