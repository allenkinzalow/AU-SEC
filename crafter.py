from flask import Flask

import pymysql
from config import DEFAULT_DATA_TABLE

#craftQuery(dictionary)
#{"command":('update','select','insert','delete')
# "table_name":"table_name" 
# "data_id":"6bd87ed4-3add-11"
# "columns":["name","medicine"]
# "values":["jeff","DrugEx"]} -- Required for 'update','insert' only
def craftQuery(dataDict):
    command = dataDict["command"]
    if not 'table_name' in dataDict:
        table_name = DEFAULT_DATA_TABLE
    else:
        table_name = dataDict["table_name"]
    row_ID = dataDict["data_id"]
    if "columns" in dataDict:
    	column_names = dataDict["columns"]
    else:
        column_names = []
    query = """ """
    if command == "update":
         values = dataDict["values"]
         query += "UPDATE " + table_name + " SET"
         for c,item in enumerate(column_names):
             if isinstance(values[c], int):
                query += " " + item + "=" + str(values[c])
             else:
                query += " " + item + "=\"" + values[c] +"\""
             
             #if isinstance(values[c],int):
             #    query+= "%d"
             #elif isinstance(values[c],str):
             #    query+= "%s"
             if c < len(column_names) - 1:
                 query+= ", "
         query += " WHERE data_id=\"" + row_ID + "\""
         #values.append(row_ID)
         #return query,values
         return query
    elif command == "select":
         query = "SELECT "
         if column_names == []:
             query += "*"
         else:
             for c,item in enumerate(column_names):
                 query += item
                 if c < len(column_names) - 1:
                     query += ", "
         query += " FROM " + table_name + " WHERE id = " + row_ID
         return query         
    elif command == "delete":
        query += "DELETE FROM " + table_name + " WHERE id = " + row_ID
        return query
    else:
        return "INVALID COMMAND"

if __name__ == "__main__":
    request = {"command":"delete","table":"patients","data_id":"6bd87ed4-3add-11","columns":["name","medicine"],"values":["jeff","drugEx"], "table_name": "patients"}
    print(craftQuery(request))
