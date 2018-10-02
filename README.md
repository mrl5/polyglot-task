# README

## Table of contents
* [Dependencies](#dependencies)
* [Task](#task)
* [ToDo](#todo)

## Dependencies
- Python3.4 (or higher)
    - `pytest` library (if you want to run tests)
- Ruby 2.3 (or higher)
- go1.10

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
2. API for getting, sending to the worker and logging input and timings. Logs should be
saved to a file.
3. Worker responsible for the process of calculation

## ToDo
1. endpoint.rb
    [ ] generate unique hash on startup and pass it to the API
2. api.go
    [ ] take two args: endpoint hash and RPN expression
    [ ] new input.log format: `date hash input execTime`
    [ ] log StdErr in error.log. Format: `hash \n exception (also log exceptions from worker)`