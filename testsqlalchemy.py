from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()
engine = create_engine("mysql://root:170119@localhost/pythondb",
                            encoding='latin1', echo=True)
engine.connect()
with engine.connect() as connection:
    result = connection.execute("select Gcode from tbgcode")
    for row in result:
        print("Gcode:", row['Gcode'])