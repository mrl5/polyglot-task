# README

## Table of contents
* [Dependencies](#dependencies)
* [Task](#task)
* [My way](#my-way)

## Dependencies
- Python3.4 (or higher)
    - `pytest` library (if you want to run tests)
- Ruby 2.3 (or higher)

## Task
#### Input:

```
2
3 4 +
5 1 2 + 4 * + 3 -
```
Where:
- N - number of input expressions to solve
- f(x1) - first RPN expression to evaluate
- f(x2) - second RPN expression to evaluate
- f(x3) - nth RPN expression to evaluate

#### Output
```
7, 0.235
14, 0.280
```
Where:
- first field: evaluation result
- second field: evaluation time

#### Architecture
1. Endpoint interface for gathering input data (stdin) and output results (stdout)
2. API for getting , sending to the worker and logging input and timings. Logs should be
saved to a file.
3. Worker responsible for the process of calculation

## My way
1. "Worker" = Python: computes RPN expressions, throws exceptions on bad input
2. "API" (requests, spawning worker processes, logging) = Go
3. Endpoint interface: Ruby or Ruby on Rails (probably the second one)
