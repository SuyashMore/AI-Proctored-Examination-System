from flask import Flask, request,jsonify,redirect, url_for,  make_response
from flask_restful import Resource, Api, reqparse
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
api= Api(app)
app.config['SECRET_KEY']='mysecretkey'


class Result(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('hello',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    def __init__(self):
        pass
    def get(self):
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        data = {"hello": "test"}
        return jsonify(data)
    def post(self):
        print("post was called")
        headers: {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        found = Result.parser.parse_args()
        data = {"hello": "successful"}
        print(found)
        return jsonify(data)


api.add_resource(Result, '/')


if __name__ == "__main__":
    app.run(debug=True)