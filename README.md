# README

## Table of contents
* [Dependencies](#dependencies)
* [Getting started](#getting-started)
* [Troubleshooting](#troubleshooting)
* [Task](#task)
* [ToDo](#todo)

## Dependencies
- Python3.4 (or higher)
    - `pytest` library (if you want to run tests)
- Ruby 2.3 or 2.4
- go1.10

## Getting started
0. Your OS:
    - if you are not running on a GNU/Linux OS, you are on your own with debugging

1. Get the application (clone or download)
    - `git clone http://github.com/mrl5/polyglot-task.git`
    - [download](https://github.com/mrl5/polyglot-task/archive/master.zip) and extract
    - go to the application's directory `cd polyglot-task`

2. run `python3 installer.py` (this script will reproduce steps 2, 3, 4)

**OR**

2. Check for dependencies
    - Python: `python --version`
    - Ruby: `ruby --version`
    - Go: `go version`

3. Compile `api.go`
    - make sure that you are inside application's directory `pwd -P | xargs basename` (you should get `polyglot-task
`)
    - `go build api.go`
4. Make sure that `endpoint.rb`, `api` and `worker.py` are executable
    - if you are running on GNU/Linux run `chmod +x endpoint.rb api worker.py`
5. Play around
    - you can start the program by typing `./endpoint.rb` or `ruby endpoint.rb`
6. Logfiles will be stored in folder `polyglot-task-by-JK-aka-mrl5-v20` in your user's home directory (e.g. `/home/kuba/polyglot-task-by-JK-aka-mrl5-v20`)

## Troubleshooting
- `api.go` doesn't compile!
    - download the binary version from [here] (check `go_env.txt` file and check section **4** from "Getting started")
- error: `sh: /home/kuba/test/polyglot-task/api: No such file or directory`
    - there is no `api` binary file in project's directory: check sections **2** and **3** for the solution
- error: `sh: /home/kuba/test/polyglot-task/api: Permission denied`
    - your user has no permission to run `api` file: check section **4** for a solution
    - if you can't change file permission you should clone or extract the project inside your user's home directory
- "I provide valid RPN expression but I get `error` output"
    - if your RPN expression is valid your user has no permission to run `worker.py` file: check section **4** for a solution
    - if you can't change file permission you should clone or extract the project inside your user's home directory
    - if none of above works, try running `python worker.py "<your RPN_expression>"` (e.g. `python worker.py "1 1 +"`) python interpreter should give you more information about what went wrong

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
2. API for getting requests, sending to the worker and logging input and timings. Logs should be
saved to a file.
3. Worker responsible for the process of calculation

## ToDo
#### api.go
- [ ] log StdErr in error.log

[here]: https://drive.google.com/drive/folders/1nweyNIvOPzCxzVGGL3a9n_3ExE0sKnYQ?usp=sharing
