package main

import (
	"fmt"
	"os"
	"errors"
	"path/filepath"
	"os/user"
)


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

func main() {
	/* path to directory of binary version of this program */
	workDir, werr := filepath.Abs(filepath.Dir(os.Args[0]))
	checkError(werr)
	usrEnv, uerr := user.Current()
	checkError(uerr)

	/* check input syntax */
	if _, argerr := checkInput(); argerr == nil {
		fmt.Println("Work dir: " + workDir)
		fmt.Println("User dir: " + usrEnv.HomeDir)
		fmt.Println("Arg: " + os.Args[1])
	} else {
		fmt.Println(argerr)
	}
}
