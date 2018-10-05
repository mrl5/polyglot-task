package main

// https://stackoverflow.com/questions/19208725/example-for-sync-waitgroup-correct
// https://stackoverflow.com/questions/3387273/how-to-implement-resizable-arrays-in-go

import (
	"fmt"
	"sync"
	"time"
)

type mytype struct {
	id, param int
	//err error
	//output []byte
	//elapsedTime time.Duration
}

var goroutinesReturns []mytype

func dosomething(id int, millisecs int, wg *sync.WaitGroup) {
	duration := time.Duration(millisecs) * time.Millisecond
	fmt.Println("START: Function in background, duration:", duration)
	time.Sleep(duration)
	fmt.Println("DONE: Function in background, duration:", duration)
	goroutinesReturns = append(goroutinesReturns, mytype{id, millisecs})
	wg.Done()
}

func main() {
	var wg sync.WaitGroup
	const delta = 4
	wg.Add(delta)

	params := [delta]int{6000, 1500, 4000, 2000}

	for i := 0; i < delta; i++ {
		go dosomething(i, params[i], &wg)
	}

	wg.Wait()
	fmt.Println("Done")
	fmt.Println(goroutinesReturns)
}