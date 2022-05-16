package main

/*
defer [명령문]
프로그램 에서 1. 파일 작업할 때 파일 핸들 요청
2. OS에서 파일 핸들 제공
프로그램 3. 작업 완료 후 파일 핸들 반환

*/

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

type dbInfo struct {
	user     string
	pwd      string
	url      string
	engine   string
	database string
}

var db1 = dbInfo{"root", "password@", "localhost:3306", "mysql", "testdb"}

func main() {
	db := dbInfo{"root", "password@", "localhost:3306", "mysql", "testdb"}
	dataSource := db.user + ":" + db.pwd + "@tcp(" + db.url + ")/" + db.database
	conn, err := sql.Open(db.engine, dataSource)

	temp_err(err, 1, conn)

	defer conn.Close()

	_, err = conn.Exec("create table if not exists orangeTest(id varchar(255),name varchar(255))")
	temp_err(err, 2, conn)

	_, err = conn.Exec("insert into orangeTest(id,name) values('great','great')")
	temp_err(err, 3, conn)

	result, err := conn.Exec("insert into orangeTest values(?,?)", "carrot", "orange")

	temp_err(err, 4, conn)

	n, err := result.RowsAffected() // 테이블 인써트 확인방법
	if n == 1 {
		fmt.Println("complete")
	}

	temp_err(err, 5, conn)
	fmt.Println("End of Day2")

}

func temp_err(eee error, num int, conn *sql.DB) {
	if eee != nil && conn.Ping() != nil {
		fmt.Println("에러입니다. + ", num)
	}
}

// single
func single_query(conn *sql.DB) {
	var name string
	err := conn.QueryRow("select id from orangeTest where id = 'carrot'").Scan(&name)
	temp_err(err, 6, conn)

}

// multi
func multi_query(conn *sql.DB) {
	var id string
	var name1 string

	rows, err := conn.Query("select id, name from orangetest where id = 'carrot'")
	temp_err(err, 7, conn)

	defer rows.Close()

	for rows.Next() {
		err := rows.Scan(&id, &name1)
		temp_err(err, 8, conn)
		fmt.Println(id, name1)
	}

}
