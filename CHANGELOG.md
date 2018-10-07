# Changelog
All **notable** changes to this project will be documented in this file.

## [v2.0] - 2018-10-07
- `endpoint.rb` calls API **once**
- `api.go` uses **goroutines** to call `worker.py`
- `installer.py` checks for dependencies and compiles `api.go`
- new `input.log` format: `<request UUID>	<execution time>	<input expression>`
- new logfile: `requests.log`

##  v1.0 - 2018-10-02
- first official release


[v2.0]: https://github.com/mrl5/polyglot-task/compare/v1.0...v2.0
