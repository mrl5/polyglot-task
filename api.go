package main

import (
	"fmt"
	"os"
	"errors"
	"path/filepath"
	"os/user"
	"path"
	"os/exec"
	"time"
	"strconv"
	"strings"
	"flag"
)

/* worker related constants */
const (
	WORKER = "worker.py"
	ERROR_MSG = "error"
)

/* logging related constants */
const (
	APP_DIR = "polyglot-task-by-JK-aka-mrl5"
	INPUT_LOG_FILE = "input.log"
	APPDIR_PERMISSION = 0750   //owner can do anything with directory, group member can list directory and see rights, others wont see dir content
	LOGFILES_PERMISSION = 0640 //RW for owner, R for group, nothing for others (0640)
)

var endpointUUID string
var logsDir = ""
var pathToInputLog string

func setFlags() {
	/* flags related constants */
	const (
		DEFAULT_UUID = "internal"
		UUID_USAGE = "Universally Unique IDentifier of an endpoint request"
	)

	/* UUID */
	flag.StringVar(&endpointUUID, "uuid", DEFAULT_UUID, UUID_USAGE)
	flag.StringVar(&endpointUUID, "u", DEFAULT_UUID, UUID_USAGE+" (shorthand)")

	/* parse all defined flags */
	flag.Parse()
}

func checkInput() (int, error) {
	switch len(flag.Args()) {
	case 1:
		return 0, nil
	case 0:
		return -1, errors.New("API error: expected an argument")
	default:
		return -2, errors.New("API error: only one argument is accepted")
	}
}

func checkError(e error) {
	if e != nil {
		panic(e)
	}
}

func checkEnvironment(usrDir string) {
	if logsDir == "" {
		logsDir = path.Join(usrDir, APP_DIR)
	}
	pathToInputLog = path.Join(logsDir, INPUT_LOG_FILE)

	/* create logs dir if doesn't exist, ignore error when exists */
	_ = os.Mkdir(logsDir, APPDIR_PERMISSION)

	/* check if log files exists */
	os.OpenFile(pathToInputLog, os.O_RDONLY|os.O_CREATE, LOGFILES_PERMISSION)
}

func logInput(input string) {
	f, err := os.OpenFile(pathToInputLog, os.O_APPEND|os.O_WRONLY, LOGFILES_PERMISSION)
	checkError(err)
	defer f.Close()

	logLine := endpointUUID + "\t" + input
	if _, err = f.WriteString(logLine); err != nil {
		panic(err)
	}
}

func executeWorker(pathToWorker string, argument string) (error, []byte) {
	workerProcess := exec.Command(pathToWorker, argument)
	output, err := workerProcess.Output()
	return err, output
}

func main() {
	start := time.Now()
	var elapsedTime string
	setFlags()

	/* path to the directory of binary version of this program */
	workDir, workDirErr := filepath.Abs(filepath.Dir(os.Args[0]))
	checkError(workDirErr)

	usrEnv, usrEnvErr := user.Current()
	checkError(usrEnvErr)
	checkEnvironment(usrEnv.HomeDir)

	/* check input syntax */
	if _, argErr := checkInput(); argErr == nil {
		pathToWorker := path.Join(workDir, WORKER)
		err, result := executeWorker(pathToWorker, flag.Arg(0))
		execTime := time.Since(start).Seconds()
		elapsedTime = strconv.FormatFloat(execTime, 'f', 3, 64)
		if err != nil {
			fmt.Println(ERROR_MSG)
		} else {
			fmt.Println(strings.Trim(string(result), "\n") + ", " + elapsedTime)
		}
	} else {
		fmt.Println(argErr)
	}
	logInput(elapsedTime + "\t" + flag.Arg(0) + "\n")
}
