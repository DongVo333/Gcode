import pandas as pd
import sqlalchemy as db
import pymysql
pymysql.install_as_MySQLdb()
engine = db.create_engine("mysql://root:170119@localhost/pythondb",
                            encoding='latin1', echo=True)
metadata = db.MetaData()                            
connection = engine.connect()
""" with engine.connect() as connection:
    result = connection.execute("select Gcode from tbgcode")
    for row in result:
        print("Gcode:", row['Gcode']) """
emp = db.Table('tbgcode', metadata, autoload=True, autoload_with=engine)
# Update record
""" query = db.update(emp).values(Description = "Hang hoa A")
query = query.where(emp.columns.Gcode == "1004")
results = connection.execute(query) """
# Insert record
#Inserting record one by one
""" query = db.insert(emp).values(Gcode='1003', Description='Pump', Kymahieu='00001352334',NSXCode = 'ABC') 
ResultProxy = connection.execute(query) """
#Inserting many records at ones
""" query = db.insert(emp) 
values_list = [{'Gcode':'1005', 'Description':'Pump', 'Kymahieu':'00001352334','NSXCode' : 'CCC'},
               {'Gcode':'1006', 'Description':'Compressor', 'Kymahieu':'333330003','NSXCode' : 'BBB'}]
ResultProxy = connection.execute(query,values_list) """
# Build a statement to delete record
""" query = db.delete(emp)
query = query.where(emp.columns.NSXCode == 'CCC')
results = connection.execute(query) """