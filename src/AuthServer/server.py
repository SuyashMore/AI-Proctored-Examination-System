from flask import Flask, request,jsonify,redirect, url_for,  make_response
from flask_restful import Resource, Api, reqparse
import os
from werkzeug.utils import secure_filename
from auth_functions import authFunctions

app = Flask(__name__)
api= Api(app)
app.config['SECRET_KEY']='mysecretkey'
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
        print("Adding User Called")
        headers: {"Accept": "application/json","Content-type": "application/json",}
        response = self.parser.parse_args()
        print(response)
        result = {"Result":400}
        # print(response['name'])
        result = authFunc.addStudent(0,response['name'],
                            response['email'],
                            response['photo_url'],
                            response['password'])

        return jsonify({'userAdded':'Success'})


api.add_resource(AddStudent, '/addUser')

if __name__ == "__main__":
    app.run(debug=True)