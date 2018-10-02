package main

import (
	"fmt"
	"os"
	"errors"
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

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	/* path to binary version of this program */
	pathToProgram := os.Args[0]

	/* check input syntax */
	if _, e := checkInput(); e == nil {
		fmt.Println("Path: " + pathToProgram)
		fmt.Println("Arg: " + os.Args[1])
	} else {
		check(e)
	}
}
