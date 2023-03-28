import os
from flask import Flask, request, jsonify, url_for, session,render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db , User,Character,Planet,Vehicle, favoritosplanetas, favoritospersonajes, favoritosvehiculos
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

app.url_map.slashes=False
app.config['DEBUG']=True
app.config['ENV']='development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] ="cualquier_palabra"
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DATABASE_URI')

db.init_app(app)
Migrate = Migrate(app,db) # db init, db migrate, db upgrade
CORS(app, resources={r"/api/*": {"origins": "*"}})
#setup_admin(app)

#ruta por default
@app.route("/")
def home():
    return render_template('index.html')

## Ruta de usuario
@app.route('/api/users', methods=['GET'])
def getuser():
    try:
        users = User.query.all()
        users = list(map(lambda user: user.serialize(),users))
      #  print({"es iterable users desde GET?"},dir(users))
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"msg": "No existe aun ningun usuario"})
    #test de getUser exitoso, pendiente Post de user

@app.route('/api/userspost', methods= ['POST'])
def create_user():
   # try:
        name = request.json.get('name')
        lastname = request.json.get('lastname')
        email = request.json.get('email')
        password = request.json.get('password')
        #favoritosplanetas = request.json.get('favoritosplanetas')
        #favoritospersonajes = request.json.get('favoritospersonajes')
        #favoritosvehiculos = request.json.get('favoritosvehiculos')
       # peticion = request.get_json()
        #print(peticion)
        #datos = request.get_json()
        user = User()
        user.name = name
        user.lastname = lastname
        user.email = email
        user.password = password
       # user.favoritosplanetas= favoritosplanetas
       # user.favoritospersonajes= favoritospersonajes
       # user.favoritosvehiculos= favoritosvehiculos
       ## print(user)
      #  db.session.add(user)
      #  db.session.commit()
        user.save() # ejecuta add + commit
       # user.get_users()

       # print({"es iterable users desde POST?"},dir(users))
        return jsonify(user.serialize_favoritos_user()), 201
       # return render_template('crea_user.html',user=user)
    #except Exception as e:
    #    print(e)
    #    return jsonify({"msg":"No se pudo agregar User"}), 400
    
##  Se mantiene pendiente validacion de POST en user
# # Recursos planet-personajes-vehicles ok con CRUD  

@app.route('/api/updateUsers/<int:id>', methods=['PUT'])
def update_user(id):
    # UPDATE user SET name="", lastname="" email="", password="" WHERE id = ?
    try:
        email =  request.json.get('email') # None
        password =  request.json.get('password') # None
        name = request.json.get('name') # None
        lastname = request.json.get('lastname') # None
        # SELECT * FROM users WHERE id = ?
        user = User.query.get(id)
        user.email = email
        user.password = password
        user.name = name
        user.lastname = lastname
        user.update()
       # print({"es iterable users desde PUT?"},dir(users))
        return jsonify(user.serialize()), 202
    except Exception as e:
    #db.session.commit()

        return jsonify({"No se logro actualizar el cambio"}), 400

@app.route('/api/deletUsers/<int:id>', methods=['DELETE'])
def delete_user(id):
    # SELECT * FROM users WHERE id = ?
    try:
        user = User.query.get(id)

        user.delete()
       # print({"es iterable users desde DELETE?"},dir(users))
        return jsonify({ "message": "User Deleted" }), 202
    except Exception as e:

        return jsonify({ "message": "No se logro eliminar a usuario" }), 400
#
##
##

####Funcion para salvar api de personajes desde la web y almacenar su info directo a la BD
@app.route('/api/almacenaPersonaje', methods=["GET"])
def almacenaPersonaje():
    #print("1")
    url ='https://www.swapi.tech/api/people'

    datos = requests.get(url)
    personajes = datos.json()
    #print({"soy data"},datos.status_code)
    #print(personajes['results'])
   
    if datos.status_code == 200:
        print("Acceso correcto")
    else:
        print("Acceso con problemas")
  
    for personaje in personajes["results"]:

        character = Character()
        character.name = personaje['name']
        character.url = personaje['url']
        character.uid = personaje['uid']
        character.save()
        
        characters = Character.query.all()
        characters= list(map(lambda character: character.serialize(), characters))
  
    return jsonify(characters), 200
@app.route('/api/getCharacter',methods=["GET"])  
def getCharacter():
    try:
        characters = Character.query.all()
        characters= list(map(lambda character: character.serialize(), characters))
    
        return jsonify(characters), 200
    except Exception as e:
        return jsonify({"msg":"Falla en la carga de personajes"})

@app.route('/api/postCharacter', methods=["POST"])  
def postCharacter():
     try:
        datos = request.get_json()
        character = Character()
        character.name =datos['name']
        character.url = datos['url']
        character.uid = datos['uid']
        character.save()
    
        return jsonify(character.serialize()), 201
     except Exception as e:
        
        return jsonify({"msg":"personaje no fue agregado"}),400

@app.route('/api/updateCharacters/<int:id>', methods=['PUT'])
def updatecharacter(id):
    try:
        name = request.json.get('name') # None
        uid = request.json.get('id') # None
        url =  request.json.get('url') # None
    
        character= Character.query.get(id)
        character.name = name
        character.uid = id
        character.url = url
        character.update()

        return jsonify({"msg":"personaje actualizado"})
    except Exception as e:
        return jsonify({"msg":"personaje no actualizado"}),202
           
@app.route('/api/deletCharacters/<int:id>', methods=['DELETE'])
def deletecharacter(id):
    try:
        character = Character.query.get(id)

        character.delete()

        return jsonify({ "message": "personaje Deleted" }), 202
    except Exception as e:
        
        return jsonify({"msg":"personaje no fue agregado"}),400

 ##Funcion para salvar api de planetas desde la web y almacenar directo a la BD   
@app.route('/api/almacenaPlanetas', methods=["GET"])
def almacenaplanetas():

    url ='https://www.swapi.tech/api/planets'
    datos = requests.get(url)

    planetas = datos.json()
    #print({"soy data"},datos.status_code)
    #print(planetas['results'])
   
    if datos.status_code == 200:
        print("Acceso correcto")
    else:
        print("Acceso con problemas")
  
    for planeta in planetas["results"]:
        planet = Planet()
        planet.name = planeta['name']
        planet.url = planeta['url']
        planet.uid = planeta['uid']
        
        planet.save()
        
        planets = Planet.query.all()
        planets= list(map(lambda planet: planet.serialize(), planets))
  
    return jsonify(planets), 200

@app.route('/api/getPlanet',methods=["GET"])  
def getPlanet():
    try:
        planets = Planet.query.all()
        planets= list(map(lambda planet: planet.serialize(), planets))
        
        return jsonify(planets), 200
    except Exception as e:
        return jsonify({"msg":"Falla en la carga de planetas"})    
    
@app.route('/api/postPlanet', methods=["POST"])  
def postplanet():
    try:
        datos = request.get_json()
        planet = Planet()
        planet.name =datos['name']
        planet.url = datos['url']
        planet.uid = datos['uid']
        planet.save()
    
        return jsonify(planet.serialize()), 201
    except Exception as e:
        
        return jsonify({"msg":"planeta no fue agregado"}),400

@app.route('/api/updatePlanet/<int:id>', methods=['PUT'])
def updateplanet(id):
    try:
        name = request.json.get('name') # Puede cambiar
        uid = request.json.get('id') # Puede cambiar
        url =  request.json.get('url') # Puede cambiar
    
        planet= Planet.query.get(id)
        planet.name = name
        planet.uid = id
        planet.url = url
        planet.update()

        return jsonify({"msg":"planeta actualizado"}),202

    except Exception as e:
        
        return jsonify({"msg":"planeta no actualizado"}),400
           
@app.route('/api/deletPlanet/<int:id>', methods=['DELETE'])
def deleteplanet(id):
    try:
        planet = Planet.query.get(id)

        planet.delete()

        return jsonify({ "message": "Planet Deleted" }), 202
    except Exception as e:
        
        return jsonify({"msg":"planeta no fue Eliminado"}),400

## rutas para CRUD de planetas favoritos        
@app.route('/api/favoritosplanetas', methods=['GET'])
def get_favoritosplanetas():
    try:
        planetasFvs = favoritosplanetas.query.all()
        planetasFvs = list(map(lambda planetasFv: planetasFv.serialize(),planetasFvs))
        
        return jsonify(planetasFvs.serialize()), 200
    except Exception as e:
        return jsonify({"msg":"No tienes planetas favoritos"})




##Funcion para salvar api de vehiculos desde la web y almacenar directo en la BD
@app.route('/api/almacenaVehiculos', methods=["GET"])
def almacenavehiculos():
    #print("1")
    url ='https://www.swapi.tech/api/vehicles'

    datos = requests.get(url)
    
    vehiculos = datos.json()
    #print({"soy data"},datos.status_code)
    #print(vehicles['results'])
   
    if datos.status_code == 200:
        print("Acceso correcto")
    else:
        print("Acceso con problemas")

    for vehiculo in vehiculos["results"]:
        vehicle = Vehicle()
        vehicle.name =vehiculo['name']
        vehicle.url = vehiculo['url']
        vehicle.uid = vehiculo['uid']
        
        vehicle.save()
        
        vehicles = Vehicle.query.all()
        vehicles= list(map(lambda vehicle: vehicle.serialize(), vehicles))
  
    return jsonify(vehicles), 200

@app.route('/api/getVehicles',methods=["GET"])  
def getVehicles():
    try:
        vehicles = Vehicle.query.all()
        vehicles= list(map(lambda vehicle: vehicle.serialize(), vehicles))
    
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"msg":"Falla en la carga de vehiculos"})

    
@app.route('/api/postVehicles', methods=["POST"])  
def postvehicles():
    try:
        datos = request.get_json()
        vehicle = Vehicle()
        vehicle.name =datos['name']
        vehicle.url = datos['url']
        vehicle.uid = datos['uid']
        vehicle.save()
    
        return jsonify(vehicle.serialize()), 201
    except Exception as e:
        
        return jsonify({"msg":"vehiculo no fue agregado"}),400

@app.route('/api/updateVehicle/<int:id>', methods=['PUT'])
def updatevehicle(id):
    try:
        name = request.json.get('name') # puede cambiar
        uid = request.json.get('id') # puede cambiar
        url =  request.json.get('url') # puede cambiar
    
        vehicle= Vehicle.query.get(id)
        vehicle.name = name
        vehicle.uid = id
        vehicle.url = url
        vehicle.update()

        return jsonify({"msg":"vehicle actualizado"})
    except Exception as e:
        return jsonify({"msg":"vehicle no actualizado"}),202
           
@app.route('/api/deletVehicle/<int:id>', methods=['DELETE'])
def deletevehicle(id):
   try:
        vehicle = Vehicle.query.get(id)

        vehicle.delete()

        return jsonify({ "message": "Vehicle Deleted" }), 202
   except Exception as e:
        
        return jsonify({"msg":"vehicle no fue Eliminado"}),400

       

#with app.app_context():
   db.create_all()
if __name__ == '__main__':
    app.run()