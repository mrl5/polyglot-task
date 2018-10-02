package main

import "os"
import "fmt"

func main() {
	/* path to binary version of this program */
	pathToProgram := os.Args[0]
	//commandLineArgs := os.Args[1:]

	fmt.Println("Path: " + pathToProgram)
}
