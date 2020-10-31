from borneo import NoSQLHandle, NoSQLHandleConfig, Regions
from borneo.iam import SignatureProvider
from borneo import PutRequest, GetRequest, QueryRequest
from flask import Flask, redirect, url_for, request
from dbManager import dbManager
from datetime import datetime

app = Flask(__name__)
db = dbManager()
db.connect()
# # PutRequest requires a table name
# request = PutRequest().set_table_name('result')

# # set the value
# request.set_value({'student_id': 100, 'test_id': '3'})
# result = handle.put(request)

# # a successful put returns a non-empty version
# if result.get_version() is not None:
#    # success
#    print("Adding Value Success")
#    handle.close()

# GetRequest requires a table name
# request = GetRequest().set_table_name('result')

# # set the primary key to use
# request.set_key({'student_id': 100,'test_id': 1})
# result = handle.get(request)

# # on success the value is not empty
# if result.get_value() is not None:
#    # success
#    print("Result Received !")
#    print(result)
#    handle.close()


# # Query at table named 'users" using the field 'name' where name may match 0
# # or more rows in the table. The table name is inferred from the query
# # statement
# statement = 'select * from result where student_id = 100'
# request = QueryRequest().set_statement(statement)
# # loop until request is done, handling results as they arrive

# result = handle.query(request)
# # handle results
# # handle_results(result) # do something with results
# print("Result Received!")
# print(result)
# # if request.is_done():
# handle.close()

@app.route('/test',methods = ['POST', 'GET'])
def make_test():
    if request.method == 'POST':
       data = request.get_json()
       result = db.insertEntry("test", data)
       return "success"
    
    elif request.method == 'GET':
        now = datetime.now()
        now = now.strftime("%Y/%m/%d %H:%M:%S")
        print(request.form['test_id'])
        test = db.getEntry("test", {'test_id': request.form['test_id']} )
        print(test)
        return "success"
            
            


if __name__=="__main__":
    app.run(debug = True)
    db.close()

''' POST
{
    "test_id": 1,
    "total_marks": 30,
    "mcq": {
        "count": 20,
        "marks": 1,
        "q&a":[
                {
                    "question": "How are you?", 
                    "options":{
                        "1": "A",
                        "2": "B", 
                        "3": "C",
                        "4": "D"
                    },
                    "expected_answer": 1
                }
        ]
    },
    "subjective":{
        "count": 5,
        "marks": 2,
        "q&a":[
                {
                    "question": "How are you?", 
                    "expected_answer": "I am great"
                }
        ]
    },
    "time_limit": 90,
    "start_time": "2020-11-1 18:00:00",
    "end_time": "2020-11-1 19:30:00",
    "threshold": {
        "no-face": 50,
        "more-face":30,
        "mismatch": 30
    }
}
'''

''' GET
{
    "student_id": 1,
    "test_id":1
}
'''
