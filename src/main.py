"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import re
from flask import Flask, request, jsonify, url_for
from flask.wrappers import Response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import  db, Ong,Activity,Voluntary, Message
import requests
from flask_jwt_extended import JWTManager,create_access_token,get_jwt_identity,jwt_required

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']= os.environ.get('FLASK_APP_KEY')
jwt= JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


def swapi_to_localhost(url_swapi):
    return url_swapi.replace('https://www.swapi.tech/api/','http://localhost:3000/')



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code



# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




# registra una ONG
@app.route('/ong', methods=['POST'])

def handle_registration_ong():
    data_new_ong = request.json
    
    new_ong=Ong.create(data_new_ong)
    if new_ong is None:
        return jsonify({"message": False}),400
    return jsonify(new_ong), 200

# retorna todas las ong
@app.route('/ong', methods=['GET'])

def handle_ong():
    list_ong= Ong.query.all()
    response=list(map(lambda ong:ong.serialize(),list_ong))
       
    if response is None:
        return jsonify({"message":"something happened, try again!"}),400
    return jsonify(response), 200



# login,  retorna un token de la ONG

@app.route('/login',  methods=['POST'])

def handle_ong_login():
    ong_name= request.json.get('ong_name', None)
    password= request.json.get('password',None)
    ong= Ong.query.filter_by(ong_name=ong_name,password= password).one_or_none()
    
    if ong is not None:
        access_token= create_access_token(identity=ong.id)
        return jsonify({"token":access_token, "ong_name":ong.ong_name,"id":ong.id}),200
    else:
        return jsonify({"message":"Credentials invalid"}),401


# crea una actividad

@app.route('/activity', methods=[ 'POST'])
@jwt_required()
def handle_create_activity():

    data_new_activity = request.json
    id = get_jwt_identity()
    data_new_activity.update({"ong_id":id})
    
    new_activity=Activity.create(data_new_activity)
    if new_activity is None:
        return jsonify({"message":"something happened, try again!"}),400
    return jsonify(new_activity), 200


# retorna todas las actividades

@app.route('/activities', methods=[ 'GET'])

def handle_get_all_activities():
    all_activities=Activity.query.all()
    response=list(map(lambda activity:activity.serialize(),all_activities))
    if response is None:
        return jsonify({"message": False}),400
    return jsonify(response), 200



#borra actividades

@app.route('/activity/<int:activity_id>', methods=[ 'DELETE'])
@jwt_required()
def handle_delete_activity(activity_id):

    activity= Activity.query.filter_by(id = activity_id).one_or_none()
    
    if activity:
        response= activity.delete()
        
        if response:
           return jsonify({"message":"done"}),200    
        else:
            return  jsonify({"message":"something happened, try again!"}),400  
    else: 
        return jsonify({"message":"Not found"}),401



# registra un voluntario

@app.route('/voluntary', methods=[ 'POST'])

def handle_create_voluntary():

    data_new_voluntary = request.json
    
    new_voluntary=Voluntary.create(data_new_voluntary)
    if new_voluntary is None:
        return jsonify({"message": "something happened, try again!"}),400
    return jsonify(new_voluntary), 200


#borra voluntarios

@app.route('/voluntary/<int:voluntary_id>', methods=[ 'DELETE'])
@jwt_required()
def handle_delete_voluntary(voluntary_id):

    voluntary= Voluntary.query.filter_by(id = voluntary_id).one_or_none()
    
    if voluntary:
        response= voluntary.delete()
        
        if response:
           return jsonify({"message":"done"}),200    
        else:
            return  jsonify({"message":"something happened, try again!"}),200   
    else: 
        return jsonify({"message":"Not found"}),401

        


@app.route('/contact', methods=['POST'])

def handle_contact():
    contact = request.json
    
    contact=Message.create(contact)
    if contact is None:
        return jsonify({"message":"something happened, try again!"}),400
    return jsonify(contact), 200








# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
