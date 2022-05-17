package main

import (
	"fmt"
	"net/http"
)

type handler struct{}

func main() {

	handler := handler{}
	server := http.Server{
		Addr:    "127.0.0.1:8080",
		Handler: &handler,
	}
	server.ListenAndServeTLS("DaeCert.pem", "Daepriv.pem") //key.pem" # text. 참고 하기
	//server.ListenAndServeTLS("cert.pem", "key.pem") //key.pem"
}

// 행들러 선언 및 페이지 로드
func (h *handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "hello World")
}

// 종료 ctrl + c
// Fprintln 에서 화면에서 출력됩니다. http:// localhost:8080
