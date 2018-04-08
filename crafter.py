from flask import Flask
import pymysql

#craftQuery(dictionary)
#{"command":('update','select','insert','delete')
# "table_name":"table_name" 
# "row_id":"6bd87ed4-3add-11"
# "columns":["name","medicine"]
# "values":["jeff","DrugEx"]} -- Required for 'update','insert' only
def craftQuery(dataDict):
    command = dataDict["command"]
    table_name = dataDict["table_name"]
    row_ID = dataDict["row_id"]
    if "columns" in dataDict:
    	column_names = dataDict["columns"]
    else:
        column_names = []
    query = """ """
    if command == "update":
         values = dataDict["values"]
         query += "UPDATE " + table_name + " SET"
         for c,item in enumerate(column_names):
             query += " " + item + "="
             
             if isinstance(values[c],int):
                 query+= "%d"
             elif isinstance(values[c],str):
                 query+= "%s"
             if c < len(column_names) - 1:
                 query+= ", "
         query += " WHERE id=%s"""
         print (query)
         values.append(row_ID)
         print (values)
         return query,values
    elif command == "select":
         query = "SELECT "
         if column_names == []:
             query += "*"
         else:
             for c,item in enumerate(column_names):
                 query += item
                 if c < len(column_names) - 1:
                     query += ", "
         query += " FROM " + table_name + " WHERE id = %s"
         print (query)
         print (row_ID)
         return query,[row_ID]
    elif command == "insert":
         auth_ID = dataDict["authorized_user"] 
         values = dataDict["values"]
         query += "INSERT INTO "+ table_name +" (id,authorized_user,"
         for c,item in enumerate(column_names):
             query+=item
             if c < len(column_names) - 1:
                  query+=","
         query+=") VALUES(%s,%s,"
         for c2,value in enumerate(values):
             if isinstance(value,int):
                 query+= "%d"
             elif isinstance(value,str):
                 query+= "%s"
             if c2 < len(values) - 1:
                 query += ","
         query+=")"
         values.insert(0,auth_ID)
         values.insert(0,row_ID)
         print (query)
         print (values)
         return query,values           
    elif command == "delete":
        query += "DELETE FROM " + table_name + " WHERE id = %s"
        print (query)
        return query,[row_ID]
    else:
        return "INVALID COMMAND"

if __name__ == "__main__":
    request = {"command":"delete","table":"patients","id":"6bd87ed4-3add-11","columns":["name","medicine"],"values":["jeff","drugEx"]}
    craftQuery(request)
