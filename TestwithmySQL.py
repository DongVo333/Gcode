import mysql.connector

myconn = mysql.connector.connect(host = "localhost", 
    user = "root", passwd = "170119", database="pythondb")
print(myconn)
cur = myconn.cursor()
try:
    # tạo bảng Employee gồm 4 cột name, id, salary, và department id  
    dbs = cur.execute("create table Employee(name varchar(20) not null, "
        + "id int(20) not null primary key, salary float not null, "
        + "dept_id int not null)")
except:
    myconn.rollback()
sql = "INSERT INTO Employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)"
val = (1,"John",50.2, 21)
cur.execute(sql, val)

myconn.commit()

print(cur.rowcount, "record inserted.")
myconn.close()