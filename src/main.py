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
from models import  db, Ong,Activity,Voluntary
import requests
from flask_jwt_extended import JWTManager,create_access_token, git 

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
        return jsonify({"token":access_token, "ong_name":ong.ong_name}),200
    else:
        return jsonify({"message":"Credentials invalid"}),401


# crea una actividad

@app.route('/activity', methods=[ 'POST'])
#@jwt_required()
def handle_create_activity():

    data_new_activity = request.json
    
    new_activity=Activity.create(data_new_activity)
    if new_activity is None:
        return jsonify({"message": False}),400
    return jsonify(new_activity), 200


# retorna todas las actividades

@app.route('/activity', methods=[ 'GET'])

def handle_get_all_activities():
    all_activities=Activity.query.all()
    response=list(map(lambda activity:activity.serialize(),all_activities))
    if response is None:
        return jsonify({"message": False}),400
    return jsonify(response), 200



#borra actividades

@app.route('/activity/<int:activity_id>', methods=[ 'DELETE'])
# # @jwt_required()
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



# crea un voluntario

@app.route('/voluntary', methods=[ 'POST'])
# # @jwt_required()
def handle_create_voluntary():

    data_new_voluntary = request.json
    
    new_voluntary=Voluntary.create(data_new_voluntary)
    if new_voluntary is None:
        return jsonify({"message": False}),400
    return jsonify(new_voluntary), 200


#borra voluntarios

@app.route('/voluntary/<int:voluntary_id>', methods=[ 'DELETE'])
# # @jwt_required()
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





   
# # retorna los datos del usuario
# @app.route('/users/<int:user_id>' , methods=['GET'])

# def handle_data_user(user_id):
#     response= User.query.filter_by(id= user_id).one_or_none()
#     if response is not None:
#         return jsonify(response.serialize()),200
#     else:
#         return jsonify({"message":"Not founded"}),401



# # login,  retorna un token del usuario

# @app.route('/login',  methods=['POST'])

# def handle_user_login():
#     user_name= request.json.get('user_name', None)
#     password= request.json.get('password',None)
#     user= User.query.filter_by(username=user_name,password= password).one_or_none()
#     if user is not None:
#         access_token= create_access_token(identity=user.id)
#         return jsonify({"token":access_token, "user_id":user.id,"user_name":user.username}),200
#     else:
#         return jsonify({"message":"Credentials invalid"}),401




# #retorna todos los recursos según la naturaleza especificada
# @app.route('/<string:nature>', methods=['GET'])

# def handle_recourse(nature):
#     # las variables determinan el numero de recursos a solicitar 
#     # 
#     limit= request.args.get('limit',100)
#     page=request.args.get('page',1)
#     # solicitud a swapi de los recursos 
#     response= requests.get(f'https://www.swapi.tech/api/{nature}?page={page}&limit={limit}')
#     body=response.json()
#     #convierte las url de response en url de mi api
#     for result in body['results']:
#         result['url']= swapi_to_localhost(result['url'])
     
#      #condición para enviar todo response o solo los diccionarios de response

#     if body['previous']== None and body['next']== None:
#         return jsonify(body['results']),response.status_code
#     else:
#         body.update(
#         previous = swapi_to_localhost(body['previous']) if body['previous'] else None,
#         next= swapi_to_localhost(body['next']) if body['next'] else None,
#         )
#         return jsonify(body),response.status_code


# #retorna un recursos por su id

# @app.route('/<string:nature>/<int:nature_id>', methods=['GET'])

# def handle_one_recourse(nature, nature_id):
#     # solicitud a swapi de un recursos nature/id
#     response= requests.get(f'https://www.swapi.tech/api/{nature}/{nature_id}')
#     body= response.json()

#     if response.status_code== 200:
#         result=body['result']
#         #convierte las url de response en url de mi api
#         result['properties'].update(
#             url=swapi_to_localhost(result['properties']['url']),
#         )
#         # si existe la propiedad homeworld entonces cambia la url de homeword por url de mi api
#         if 'homeworld' in result['properties']:
#             result['properties'].update(
#             homeworld= swapi_to_localhost(result['properties']['homeworld']) 
#             )

#         return jsonify(result),response.status_code
#     else:
#         return jsonify(body),response.status_code



# #Con GET se obtiene todos los favoritos del usuario

# @app.route('/favorites', methods=['GET'])
# @jwt_required()
# def handle_favorites():
#         user= get_jwt_identity()
#         favorites= Favorite.query.filter_by(user_id = get_jwt_identity())
#         response=list(map(lambda favorite:favorite.serialize(),favorites))
       
#         return jsonify(response),200    

    
# @app.route('/favorites/add', methods=['POST'])
# @jwt_required()
# def handle_favorites_add():
#         data_favorite= request.json
#         user_id= get_jwt_identity()
#         data={
#            'url':data_favorite['url'],
#            'name_favorite':data_favorite['name_favorite'],
#            'user_id':user_id
           
#        }

#         response=Favorite.create(data)
#         if response:
#             return jsonify(response),201
#         else:
#             return jsonify( None),400



# @app.route('/favorites/delete/<int:favorite_id>', methods=[ 'DELETE'])
# # @jwt_required()
# def handle_delete_favorites(favorite_id):

#     favorite= Favorite.query.filter_by(id = favorite_id).one_or_none()
    
#     if favorite:
#         favorite.delete()
#         return jsonify({"message":"Done"}),200    
#     else: 
#         return jsonify({"message":"Not found"}),401






# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
