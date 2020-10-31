from flask import Flask, request,jsonify,redirect, url_for,  make_response
from flask_restful import Resource, Api, reqparse
import os
from werkzeug.utils import secure_filename
from test_functions import testFunction

app = Flask(__name__)
api= Api(app)
testFunc = testFunction()
testFunc.connect2DB()

class CreateTest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('test_id',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('test_details',type=dict,required=True,help="This field cannot be left blank.")

        
    def post(self):
        print("Creating Test Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        result = testFunc.createTest(response['test_id'],
                            response['test_details'])

        return jsonify({'testCreation':'Success'})

class GetTest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('test_id',type=str,required=True,help="This field cannot be left blank.")

    def post(self):
        print("get Test Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        result = testFunc.getTest(response['test_id'])

        return result

class GetAllTest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        pass

    def post(self):
        print("get Test Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        result = testFunc.getAllTest()

        return result

api.add_resource(CreateTest, '/createTest')
api.add_resource(GetTest, '/getTest')
api.add_resource(GetAllTest, '/getAllTest')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=100,debug=True)

