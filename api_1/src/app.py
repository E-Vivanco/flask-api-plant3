import os
from flask import Flask, request, jsonify, url_for, session,render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User,Character,Planet,Vehicle
import requests
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

app.url_map.slashes=False
app.config['DEBUG']=True
app.config['ENV']='development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
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
@app.route('/api/getUser', methods=['GET'])
def getuser():
    #test de getUser exitoso, pendiente Post de user
    try:
        users= User.query.all()
        list_user=list()
        print(users)
        for u in users:
            list_user.append({"email":u.email,"password": u.password,"isActive":u.isActive})
            response_body ={"msg": "Hello, this is your GET /user response "}
        return jsonify({"users":list_user}), 200
    except Exception as e:
        return jsonify({"mensaje":"No existe aun,ningun usuario "})

#  Se mantiene pendiente validacion de POST en user
# # Recursos planet-personajes-vehicles ok con CRUD  
@app.route('/api/createUsers', methods=['POST'])
def createusers():
    # INSERT INTO users() VALUES ()
    email = request.json.get('email') # None
    password = request.json.get('password') # None
    isActive =  request.json.get('isActive') # None
    
    #Pruebas con registro de uauario
    #datos = request.get_json()
    #print(datos)
    user= User()
    user = User.query.filter_by(email=email).first()
    if user: return jsonify({"msg": "Email esta en uso"}),400
    if not user:
       
        user.email = email
        user.password = password
        user.isActive = isActive
        user.save() # ejecuta add + commit

        return jsonify({"msg": "Usuario no se encuentra, creado el usuario"}), 201
        
        

    #return jsonify({"msg": "Usuario registrado"}), 201
#
#@app.route('/api/updateUsers/<int:id>', methods=['PATCH'])
#def update_user(id):
#    # UPDATE user SET name="", lastname="" email="", password="" WHERE id = ?
#    
#    email =  request.json.get('email') # None
#    password =  request.json.get('password') # None
#    isActive = request.json.get('isActive') # None
#    # SELECT * FROM users WHERE id = ?
#    user = User.query.get(id)
#    user.email = email
#    user.password = password
#    user.isActive = isActive
#    user.update()
#    
#    #db.session.commit()
#
#    return jsonify(user.serialize()), 202
#
#@app.route('/api/deletUsers/<int:id>', methods=['DELETE'])
#def delete_user(id):
#    # SELECT * FROM users WHERE id = ?
#    user = User.query.get(id)
#
#    # DELETE FROM users WHERE id=?
#    user.delete()
#
#    return jsonify({ "message": "User Deleted" }), 202
#
#
#
###Funcion para salvar api de personajes desde la web y almacenar su info en archivo
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
 #   db.create_all()

if __name__ == '__main__':
    app.run()