from flask import Flask, request,jsonify,redirect, url_for,  make_response
from flask_restful import Resource, Api, reqparse
import os
from werkzeug.utils import secure_filename
from auth_functions import authFunctions

app = Flask(__name__)
api= Api(app)
authFunc = authFunctions()
authFunc.connect2DB()

class AddStudent(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('email',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('password',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('photo_url',type=str,required=True,help="This field cannot be left blank.")

    def post(self):
        # print("Adding User Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        result = authFunc.addStudent(0,response['name'],
                            response['email'],
                            response['photo_url'],
                            response['password'])

        return jsonify({'userAdded':'Success'})

class AddAdmin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('email',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('password',type=str,required=True,help="This field cannot be left blank.")

    def post(self):
        print("Adding Admin Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        result = authFunc.addAdmin(0,response['name'],
                            response['email'],
                            response['password'])

        return jsonify({'adminAdd':'Success'})

class verifyStudent(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('password',type=str,required=True,help="This field cannot be left blank.")

    def post(self):
        print("Verify Student Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print("Request Received !")
        print(response)
        loginDetailsCorrect = authFunc.verifyStudent(response['email'],
                                response['password'])

        if(loginDetailsCorrect):
            return jsonify({'verify':'Success'})    

        return jsonify({'verify':'Fail'})

class verifyAdmin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('email',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('password',type=str,required=True,help="This field cannot be left blank.")

    def post(self):
        print("Verify Admin Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        result = {"Result":400}
        loginDetailsCorrect = authFunc.verifyAdmin(response['email'],
                            response['password'])

        if(loginDetailsCorrect):
            return jsonify({'verify':'Success'})    

        return jsonify({'verify':'Fail'})


class validateStudent(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('studentID',type=str,required=True,help="This field cannot be left blank.")
        self.parser.add_argument('imageURL',type=str,required=True,help="This field cannot be left blank.")

    def post(self):
        print("Validate Student Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        validStudent = authFunc.validateStudent(response['studentID'],
                            response['imageURL'])
        if validStudent:
            return jsonify({'validation':'Success'})

        return jsonify({'validation':'Fail'})





api.add_resource(AddStudent, '/addStudent')
api.add_resource(AddAdmin, '/addAdmin')
api.add_resource(verifyStudent, '/verifyStudent')
api.add_resource(verifyAdmin, '/verifyAdmin')
api.add_resource(validateStudent, '/validateStudent')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=300,debug=True)

