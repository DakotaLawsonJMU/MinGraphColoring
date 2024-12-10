# Running a solver
All test inputs are found in the `test_cases` directory
`minGraphColorSolver.py` solves the min graph color problem
`minGraphColorGreedy.py` approximates a solution with a greedy strategy
`minGraphColorAnnealing.py` approximates a solution with an annealing strategy
To run a particular algorithm on a particular input run `python3 <solver> <input> <output>`
For example `python3 minGraphColorSolver.py test_cases/tiny.txt temp` computes the exact solution for the tiny test case and stores the solution in `temp`
To run all algorithms on all test cases use the `run_test_cases.sh` shell script
