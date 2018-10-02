package main

import (
	"fmt"
	"strconv"
	"os"
)

func main() {
	/* path to binary version of this program */
	pathToProgram := os.Args[0]
	fmt.Println("Path: " + pathToProgram)

	if len(os.Args) > 1 {
		for i := 1; i < len(os.Args); i++ {
			fmt.Println("Arg " + strconv.Itoa(i) + ": "+ os.Args[i])
		}
	}
}
