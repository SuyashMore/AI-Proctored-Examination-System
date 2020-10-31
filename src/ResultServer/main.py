from flask import Flask, request,jsonify,redirect, url_for,  make_response
from flask_restful import Resource, Api, reqparse
import os
from dbManager import dbManager


app = Flask(__name__)
api= Api(app)
app.config['SECRET_KEY']='mysecretkey'

class getStudentResult(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('student_id', type=str, required=True, help="This field cannot be left blank.")
    def __init__(self):
        db.connect()
  
    def post(self):
        print("post was called")
        headers: { "Accept": "application/json", "Content-type": "application/json",}
        found =getStudentResult.parser.parse_args()["student_id"]
        query = "SELECT * FROM result where student_id=" + found
        result = db.runQuery(str(query))
        bigjson = []
        for r in result :
            jsondata = {
                'student_id': r["student_id"], 
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
    parser.add_argument('student_id', type=str, required=True, help="This field cannot be left blank.")
    parser.add_argument('test_id', type=str, required=True, help="This field cannot be left blank.")
    def __init__(self):
        db.connect()
    
    def post(self):
        print("post student response was called")
        headers: { "Accept": "application/json", "Content-type": "application/json",}
        s_id = getStudentResponse.parser.parse_args()["student_id"]
        t_id = getStudentResponse.parser.parse_args()["test_id"]
        query = "SELECT * FROM result where test_id=" + t_id + " and student_id=" + s_id
        result = db.runQuery(str(query))
        bigjson = []
        for r in result :
            jsondata = {
                'student_id': r["student_id"], 
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


api.add_resource(getStudentResult, '/getStudentResult')
api.add_resource(getTestResult, '/getTestResult')
api.add_resource(getStudentResponse, '/getStudentResponse')

if __name__ == "__main__":
    db = dbManager()
    app.run(debug=True)