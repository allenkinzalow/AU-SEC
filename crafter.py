from flask import Flask
import mysql.connector


#craftQuery(dictionary)
#{"command":('update','select','insert','delete')
# "table":"table_name" 
# "id":"6bd87ed4-3add-11"
# "columns":["name","medicine"]
# "values":["jeff","DrugEx"]} -- Required for 'update','insert' only
def craftQuery(dataDict):
    command = dataDict["command"]
    table_name = dataDict["table"]
    user_ID = dataDict["id"]
    column_names = dataDict["columns"]
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
         values.append(user_ID)
         print (values)
         return query,values
    elif command == "select":
         
    elif command == "insert":
         values = dataDict["values"]
         query += "INSERT INTO patients(id,"
         for c,item in enumerate(column_names):
             query+=item
             if c < len(column_names) - 1:
                  query+=","
         query+=") VALUES(%s,"
         for c2,value in enumerate(values):
             if isinstance(value,int):
                 query+= "%d"
             elif isinstance(value,str):
                 query+= "%s"
             if c2 < len(values) - 1:
                 query += ","
         query+=")"
         values.insert(0,user_ID)
         print (query)
         print (values)
         return query,values           
    elif command == "delete":
        query += "DELETE FROM " + table_name + " WHERE id = %s"
        return query,[user_id]
    else:
        return "INVALID COMMAND"

if __name__ == "__main__":
    request = {"command":"update","table":"patients","id":"6bd87ed4-3add-11","columns":["name","medicine"],"values":["jeff","drugEx"]
    craftQuery(request)
