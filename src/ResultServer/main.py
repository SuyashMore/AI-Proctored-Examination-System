from flask import Flask, request,jsonify,redirect, url_for,  make_response
from flask_restful import Resource, Api, reqparse
import os
from dbManager import dbManager
import random



app = Flask(__name__)
api= Api(app)
app.config['SECRET_KEY']='mysecretkey'

class getStudentResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('studentEmail', type=str, required=True, help="This field cannot be left blank.")
    def __init__(self):
        db.connect()
  
    def post(self):
        print("post was called")
        headers: { "Accept": "application/json", "Content-type": "application/json",}
        found =getStudentResult.parser.parse_args()["studentEmail"]
        query = "SELECT * FROM result where email='" + found+"'"
        result = db.runQuery(str(query))
        bigjson = []
        for r in result :
            jsondata = {
                'student_id': r["student_id"], 
                'email': r["email"],
                'test_id': r["test_id"],
                'mcq_score':r['mcq_score'],
                'final_score':r['final_score'],
                'generated':r['generated'],
                'answers':r['answers'],
                'integrity':r['integrity'],
                'subjective_score':r['subjective_score']
            }
            bigjson.append(jsondata)
        
        data = {"result": bigjson}
        return jsonify(data)

class getTestResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('test_id', type=str, required=True, help="This field cannot be left blank.")
    def __init__(self):
        db.connect()
    
    def post(self):
        print("post test was called")
        headers: { "Accept": "application/json", "Content-type": "application/json",}
        found =getTestResult.parser.parse_args()["test_id"]
        query = "SELECT * FROM result where test_id=" + found
        result = db.runQuery(str(query))
        bigjson = []
        for r in result :
            jsondata = {
                'student_id': r["student_id"], 
                'email':r["email"],
                'test_id': r["test_id"],
                'mcq_score':r['mcq_score'],
                'final_score':r['final_score'],
                'generated':r['generated'],
                'answers':r['answers'],
                'integrity':r['integrity'],
                'subjective_score':r['subjective_score']
            }
            bigjson.append(jsondata)
        
    
        data = {"result": bigjson}
        return jsonify(data)

class getStudentResponse(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('studentEmail', type=str, required=True, help="This field cannot be left blank.")
    parser.add_argument('test_id', type=str, required=True, help="This field cannot be left blank.")
    def __init__(self):
        db.connect()
    
    def post(self):
        print("post student response was called")
        headers: { "Accept": "application/json", "Content-type": "application/json",}
        s_email = getStudentResponse.parser.parse_args()["studentEmail"]
        t_id = getStudentResponse.parser.parse_args()["test_id"]
        query = "SELECT * FROM result where test_id=" + t_id + " and email='" + s_email+"'"
        result = db.runQuery(str(query))
        bigjson = []
        for r in result :
            jsondata = {
                'student_id': r["student_id"], 
                'email': r["email"],
                'test_id': r["test_id"],
                'mcq_score':r['mcq_score'],
                'final_score':r['final_score'],
                'generated':r['generated'],
                'answers':r['answers'],
                'integrity':r['integrity'],
                'subjective_score':r['subjective_score']
            }
            bigjson.append(jsondata)
    
        data = {"result": bigjson}
        return jsonify(data)

class scoreAndStore(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('response', type=dict, required=True, help="This field cannot be left blank.")
    
    def __init__(self):
        db.connect()
    
    def post(self):
        print("score and store was called")
        headers: { "Accept": "application/json", "Content-type": "application/json",}
        response = scoreAndStore.parser.parse_args()["response"]
        print(type(response))
        t_id = str(response["testID"])
        email = str(response["studentEmail"])
        s_id = random.randint(0,20000)
        mcq_score =random.randint(1,5)
        final_score=mcq_score+random.randint(1,5)
        generated=False
        answers=[]
        integrity=random.randint(1,100)
        subjective_score=random.randint(1,20)
        qna = response["qna"]
        for q in qna:
            if(q["actualAnswer"]!="This is a sbjective question"):
                if(q["actualAnswer"]==q["studentAnswer"]):
                    mcq_score = mcq_score +1
            answers.append(q["studentAnswer"])
        print(qna)
        print(type(qna))
        print(mcq_score)
        print(answers)
        
        jsondata = {
                'student_id': s_id,
                'email':email,
                'test_id': t_id,
                'mcq_score':mcq_score,
                'final_score':final_score,
                'generated':generated,
                'answers':answers,
                'integrity':integrity,
                'subjective_score':subjective_score
            }

        

        result = db.insertEntry("result",jsondata)
        print(result)
        
        data = {"result": "success"}
        return jsonify(data)


api.add_resource(getStudentResult, '/getStudentResult')
api.add_resource(getTestResult, '/getTestResult')
api.add_resource(getStudentResponse, '/getStudentResponse')
api.add_resource(scoreAndStore, '/scoreAndStore')

if __name__ == "__main__":
    db = dbManager()
    app.run(host='0.0.0.0', port=200,debug=True)








'''

Response of Student
{
  testID: '69',
  studentEmail: 'HelloWorld@google.com',
  qna: [
    { ind: 1, studentAnswer: '4', actualAnswer: '4' },
    {
      ind: 2,
      studentAnswer: 'jaf;ioejosdc ijdo oajsodjao',
      actualAnswer: 'This is a sbjective question'
    }
  ]
}
{
  id: '69',
  questions: [
    {
      answer: '4',
      ind: 1,
      op1: 'sky',
      op2: 'cloud',
      op3: 'ceiling',
      op4: 'Oracle cloud',
      question: 'What is up'
    },
    { ind: 2, question: 'What is the best' }
  ],
  testDuration: '69',
  warningThreshold: '6'
}
#####

{
    "response" : {
        "testID" : 2,
        "studentEmail" : "hdg@oracle.com",
        "student_id": 100,
        "qna" : [
            {
                "ind": 1,
                "studentAnswer": "parht wafdgfgcfbjbocnbkcjnbgk",
                "actualAnswer": "This is a sbjective question"
            },
            { 
                "ind": 2, 
                "studentAnswer": "4", 
                "actualAnswer": "4" 
            },
            { 
                "ind": 2, 
                "studentAnswer": "4", 
                "actualAnswer": "4" 
            },
            { 
                "ind": 2, 
                "studentAnswer": "hekko", 
                "actualAnswer": "hekko" 
            }
        ]
        
    }
}
'''


