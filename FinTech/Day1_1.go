package main

/*
채널의 개념 멀티 쓰레스 개념

해당 메소드가 돌아 갈때 까지 시간이 걸릴때
미리 실행된 메소드가 가지고 있는 개념입니다.

*/

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println(123)

	// 멀티 쓰레스 개념
	c1 := make(chan bool)

	start := time.Now()
	//... operation that takes 20 milliseconds ...

	for i := 1; i < 10; i++ {
		go odd(c1, i)
		fmt.Println(c1)
	}

	//t := time.Now()
	elapsed := time.Since(start)
	fmt.Println(elapsed)

	start1 := time.Now()

	for i := 1; i < 10; i++ {
		c2 := <-c1
		fmt.Println(c2)
	}
	elapsed1 := time.Since(start1)
	fmt.Println(elapsed1)

}

func odd(mychan chan bool, num int) (bool, int) {
	//temp2 := make(chan bool)
	if num%2 == 1 {
		mychan <- true
		//fmt.Println(temp2)
		return true, num
	} else {
		mychan <- false
		//fmt.Println(temp2)

		//??
		return false, num
	}
	//fmt.Println(temp2)

}
