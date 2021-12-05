from flask import Flask,request,make_response
from flask.templating import render_template
from flask_restful import Api,Resource,reqparse
from datetime import date,datetime

app = Flask(__name__)
api =  Api(app)
class Room(Resource):
    def __init__(self):
        pass
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete():
        pass    
    
    
class User(Resource):
    def __init__(self):
        pass
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete():
        pass    
    
class Message(Resource):
    def __init__(self):
        pass
    
    def get(self):
        pass
    
    def post(self):
        pass

    def put(self):
        pass
    
    def delete():
        pass    

class HomePage(Resource):
    def __init__(self):
        pass
    
    def get(self):
        headers = {'name': 'daniel'}
        return make_response(render_template('index.html',utc_dt=datetime.utcnow()))
    
    def post(self):
        pass

    def put(self):
        pass
    
    def delete():
        pass    

api.add_resource(HomePage, "/")

class Window(Resource):
    def __init__(self):
        pass
    
    def get(self):
        username = request.args.get('username')
        roomname = request.args.get('roomname')
        return make_response(render_template('window.html',username=username,roomname=roomname))
    
    def post(self):
        pass

    def put(self):
        pass
    
    def delete():
        pass    

api.add_resource(Window, "/window")
if __name__ == "__main__":
    app.run(debug=True)