import mysql.connector

# MySQL 연결 설정
mysql_host = "mysql"
mysql_port = 3306
mysql_user = "db_user"
mysql_password = "db_password"
mysql_database = "mydatabase"

# MySQL 연결
connection = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

# 쿼리 실행 예제
cursor = connection.cursor()
cursor.execute("SELECT * FROM your_table")
result = cursor.fetchall()
for row in result:
    print(row)

# 연결 종료
connection.close()
