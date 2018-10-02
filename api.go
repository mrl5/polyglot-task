package main

import (
	"fmt"
	"os"
	"errors"
	"path/filepath"
	"os/user"
	"path"
)

var logsDir = ""
const APP_DIR string = "polyglot-task-by-JK-aka-mrl5"
const INPUT_LOG_FILE string = "input.log"
const APPDIR_PERMISSION = 0750 //owner can do anything with directory, group member can list directory and see rights, others wont see dir content
const LOGFILES_PERMISSION = 0640 //RW for owner, R for group, nothing for others (0640)
var pathToInputLog string

func checkInput() (int, error) {
	switch len(os.Args) {
	case 2:
		return 0, nil
	case 1:
		return -1, errors.New("error: expected an argument")
	default:
		return -2, errors.New("error: only one argument is accepted")
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
	checkForFile(pathToInputLog)
}

func checkForFile(pathToFile string) {
	/** checks if file exists
	 *  creates when doesn't
	 */
	os.OpenFile(pathToFile, os.O_RDONLY|os.O_CREATE, LOGFILES_PERMISSION)
}

func logInput(input string) {
	f, err := os.OpenFile(pathToInputLog, os.O_APPEND|os.O_WRONLY, LOGFILES_PERMISSION)
	if err != nil {
		panic(err)
	}

	defer f.Close()

	if _, err = f.WriteString(input); err != nil {
		panic(err)
	}
}

func main() {
	/* path to directory of binary version of this program */
	workDir, workDirErr := filepath.Abs(filepath.Dir(os.Args[0]))
	checkError(workDirErr)
	usrEnv, usrEnvErr := user.Current()
	checkError(usrEnvErr)

	checkEnvironment(usrEnv.HomeDir)

	/* check input syntax */
	if _, argErr := checkInput(); argErr == nil {
		fmt.Println("Work dir: " + workDir)
		fmt.Println("Logs dir: " + logsDir)
		fmt.Println("Arg: " + os.Args[1])
		logInput(os.Args[1] + "\n")
	} else {
		fmt.Println(argErr)
	}
}
