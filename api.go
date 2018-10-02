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

func main() {
	/* path to binary version of this program */
	pathToProgram := os.Args[0]
	fmt.Println("Path: " + pathToProgram)

	if r, e := checkInput(); e == nil {
		fmt.Println("Arg: " + os.Args[1])
	} else {
		fmt.Println("return code: ", r)
		fmt.Println(e)
	}
}
