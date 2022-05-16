package main

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

	temp_err(err, 1)

	defer conn.Close()

	_, err = conn.Exec("create table if not exists orangeTest(id varchar(255),name varchar(255))")
	temp_err(err, 2)

	_, err = conn.Exec("insert into orangeTest(id,name) values('great','great')")
	temp_err(err, 3)

	result, err := conn.Exec("insert into orangeTest values(?,?)", "carrot", "orange")

	temp_err(err, 4)

	n, err := result.RowsAffected() // 테이블 인써트 확인방법
	if n == 1 {
		fmt.Println("complete")
	}

	temp_err(err, 5)
	fmt.Println("End of Day2")

}

func temp_err(eee error, num int) {
	if eee != nil {
		fmt.Println("에러입니다. + ", num)
	}
}
