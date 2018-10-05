package main

// https://stackoverflow.com/questions/19208725/example-for-sync-waitgroup-correct
// https://stackoverflow.com/questions/3387273/how-to-implement-resizable-arrays-in-go
// https://gist.github.com/dnutiu/a899e48c95ff80fe98bada566e03251e

import (
	"fmt"
	"sync"
	"time"
	"sort"
)

type mytype struct {
	id, param int
	//err error
	//output []byte
	//elapsedTime time.Duration
}

type mytypeArr []mytype
var returns mytypeArr

func dosomething(id int, millisecs int, wg *sync.WaitGroup) {
	duration := time.Duration(millisecs) * time.Millisecond
	fmt.Println("START: Function in background, duration:", duration)
	time.Sleep(duration)
	fmt.Println("DONE: Function in background, duration:", duration)
	returns = append(returns, mytype{id, millisecs})
	wg.Done()
}

func (s mytypeArr) Len() int {
	return len(s)
}

func (s mytypeArr) Less(i, j int) bool {
	return s[i].id < s[j].id
}

func (s mytypeArr) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
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

	fmt.Println(returns)
	fmt.Println(sort.IsSorted(returns))
	sort.Sort(returns)
	fmt.Println(returns)
	fmt.Println(sort.IsSorted(returns))
	sort.Sort(sort.Reverse(returns))
	fmt.Println(returns)

}