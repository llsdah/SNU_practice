package main

// nim == null
import (
	"fmt"
	"runtime"
	"testing"
	"time"
)

func main() {

	fmt.Println(123)
	//	mylib.Maps()
	row := 10
	column := 10

	temp2 := widthes(row, column)

	//(row, column)
	fmt.Println(temp2)
	fmt.Println(runtime.NumCPU())
	timeTest()
	num12 := num1
	fmt.Println(num12)

	/*
		c1 := make(chan int)

		go func() {
			c1 <- 123
		}()

		go func() {
			temp := <-c1
			fmt.Println("%d", temp)
			}()
		time.Sleep(time.Second * 3)
	*/
	// 멀티 쓰레스 개념
	c1 := make(chan bool)
	for i := 1; i < 10; i++ {
		go odd(c1, i)
		fmt.Println(c1)
	}

	defer close(c1)

}

func TestSUm(t *testing.T) {
	s := calc.Sum(1, 2, 4)

	if s != 6 {
		fmt.Println(s)
	}
}

type P struct {
	width, height int
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

	// _, err := sql.

	return false, 0
}

func num1(p *P) int {
	p.width = 10
	p.height = 12
	return p.width * p.height
}

func timeTest() {
	go fmt.Print("go rutine")

	fmt.Println("12")
	time.Sleep(time.Second * 3)
}

func widthes(row int, column int) int {

	return row * column
}

func Maps() {
	infos := map[string]string{"name": "lemon", "age": "12"}
	for key, value := range infos {
		fmt.Println(key, value)
	}
	for _, value := range infos {
		// _ 쓰면 안써도 에러나는 것 방지 할 수 있다.
		fmt.Println(value)
	}
}

func structt() {

	type temp struct {
		x, y, c float64
	}

	//var z temp // == c := new(temp)
	//z := new(temp)
	z := temp{}
	z.x = 5
	z.y = 5
	z.c = 6
	//c := temp{x: 0, y: 0, c: 5}
	//c.x

}
