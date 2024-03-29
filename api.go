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
	"sync"
	"sort"
)

/* worker related constants */
const (
	WORKER = "worker.py"
	ERROR_MSG = "error"
)

/* logging related constants */
const (
	APP_DIR = "polyglot-task-by-JK-aka-mrl5-v20"
	INPUT_LOG_FILE = "input.log"
	REQUESTS_LOG_FILE = "requests.log"
	APPDIR_PERMISSION = 0750   //owner can do anything with directory, group member can list directory and see rights, others wont see dir content
	LOGFILES_PERMISSION = 0640 //RW for owner, R for group, nothing for others (0640)
)

var endpointUUID string
var logsDir = ""
var pathToInputLog string
var pathToRequestsLog string

func setFlags() {
	/* flags related constants */
	const (
		defaultUUID = "internal"
		uuidUsage = "Universally Unique IDentifier of the endpoint request"
	)

	/* UUID */
	flag.StringVar(&endpointUUID, "uuid", defaultUUID, uuidUsage)
	flag.StringVar(&endpointUUID, "u", defaultUUID, uuidUsage+" (shorthand)")

	/* parse all defined flags */
	flag.Parse()
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
	pathToRequestsLog = path.Join(logsDir, REQUESTS_LOG_FILE)

	/* create logs dir if doesn't exist, ignore error when it exists */
	_ = os.Mkdir(logsDir, APPDIR_PERMISSION)

	/* check if log files exist, create when they don't */
	os.OpenFile(pathToInputLog, os.O_RDONLY|os.O_CREATE, LOGFILES_PERMISSION)
	os.OpenFile(pathToRequestsLog, os.O_RDONLY|os.O_CREATE, LOGFILES_PERMISSION)
}

func checkInput(noOfArgs int) (int, error) {
	switch noOfArgs {
	default:
		return 0, nil
	case 0:
		return -1, errors.New("API error: expected at least one argument")
	}
}

func logInput(input string, elapsedProcessTime string) {
	f, err := os.OpenFile(pathToInputLog, os.O_APPEND|os.O_WRONLY, LOGFILES_PERMISSION)
	checkError(err)
	defer f.Close()

	/* uuid elapsed-time input */
	logLine := endpointUUID + "\t" + elapsedProcessTime + "\t" + input + "\n"
	if _, err = f.WriteString(logLine); err != nil {
		panic(err)
	}
}

func logRequest(requestStart time.Time, noOfArguments int) {
	f, err := os.OpenFile(pathToRequestsLog, os.O_APPEND|os.O_WRONLY, LOGFILES_PERMISSION)
	checkError(err)
	defer f.Close()

	/* date uuid elapsed-time number-of-args */
	logLine := "[" + requestStart.UTC().String() + "]\t" + endpointUUID + "\t"  +
		strconv.FormatFloat(time.Since(requestStart).Seconds(), 'f', 3, 64) + "\t" +
		strconv.Itoa(noOfArguments) + "\n"
	if _, err = f.WriteString(logLine); err != nil {
		panic(err)
	}
}


/* goroutines framework */
type workerReturn struct {
	id int
	err error
	output []byte
	elapsedTime time.Duration
}

type workerReturnArr []workerReturn
var workerReturns workerReturnArr

func (wr workerReturnArr) Len() int {
	return len(wr)
}

func (wr workerReturnArr) Less(i, j int) bool {
	return wr[i].id < wr[j].id
}

func (wr workerReturnArr) Swap(i, j int) {
	wr[i], wr[j] = wr[j], wr[i]
}
/* /goroutines framework */

func executeWorker(pathToWorker string, argument string, id int, wg *sync.WaitGroup) {
	start := time.Now()
	workerProcess := exec.Command(pathToWorker, argument)
	output, err := workerProcess.Output()
	/* add return to the array of returns */
	workerReturns = append(workerReturns, workerReturn{id, err, output, time.Since(start)})
	wg.Done()
}

func main() {
	start := time.Now()
	setFlags()

	/* path to the directory of binary version of this program */
	workDir, workDirErr := filepath.Abs(filepath.Dir(os.Args[0]))
	checkError(workDirErr)
	pathToWorker := path.Join(workDir, WORKER)

	usrEnv, usrEnvErr := user.Current()
	checkError(usrEnvErr)
	checkEnvironment(usrEnv.HomeDir)

	noOfArgs := len(flag.Args())

	if _, argErr := checkInput(noOfArgs); argErr == nil {
		/* sync.WaitGroup waits for a group of goroutines to finish */
		var wg sync.WaitGroup
		wg.Add(noOfArgs)

		for i := 0; i < noOfArgs; i++ {
			go executeWorker(pathToWorker, flag.Arg(i), i, &wg)
		}
		/* wait until all executeWorker processes will end */
		wg.Wait()
		/* FIFO sorting (by id) */
		sort.Sort(workerReturns)

		for i := 0; i < noOfArgs; i++ {
			var result string
			formattedTime := strconv.FormatFloat(
				workerReturns[i].elapsedTime.Seconds(), 'f', 3, 64)

			if workerReturns[i].err != nil {
				result = ERROR_MSG
			} else {
				result = strings.Trim(
					string(workerReturns[i].output), "\n")
			}
			fmt.Println(result + ", " + formattedTime)
			logInput(flag.Arg(i), formattedTime)
		}

	} else {
		fmt.Println(argErr)
	}
	logRequest(start, len(flag.Args()))
}
