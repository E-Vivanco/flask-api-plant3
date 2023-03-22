import os
from flask import Flask, request, jsonify, url_for, session,render_template
from flask_migrate import Migrate
from flask_cors import CORS
from models import db,User,Character,Planet,Vehicle
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

@app.route("/")
def home():
    return render_template('index.html')

## Ruta de usuario
@app.route('/api/users', methods=['GET'])
def get_users():

    # SELECT * FROM users;
    users = User.query.all() 
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    # INSERT INTO users() VALUES ()

    datos = request.get_json()
    user = User()
    user.name = datos['name']
    user.lastname = datos['lastname']
    user.email = datos['email']
    user.password = datos['password']
    user.isActive = datos['isActive']
    user.save() # ejecuta add + commit


    return jsonify(user.serialize()), 201

@app.route('/api/users/<int:id>', methods=['PATCH'])
def update_user(id):
    # UPDATE user SET name="", lastname="" email="", password="" WHERE id = ?
    
    name = request.json.get('name') # None
    lastname = request.json.get('lastname') # None
    email =  request.json.get('email') # None
    password =  request.json.get('password') # None

    # SELECT * FROM users WHERE id = ?
    user = User.query.get(id)
    user.name = name
    user.lastname = lastname
    user.email = email
    user.password = password
    user.update()
    
    #db.session.commit()

    return jsonify(user.serialize()), 202

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    # SELECT * FROM users WHERE id = ?
    user = User.query.get(id)

    # DELETE FROM users WHERE id=?
    user.delete()

    return jsonify({ "message": "User Deleted" }), 202



##Funcion para salvar api de personajes desde la web y almacenar su info en archivo
@app.route('/api/almacenaPersonaje', methods=["GET"])
def almacenaPersonaje():
    #print("1")
    url ='https://www.swapi.tech/api/people'

    datos = requests.get(url)
    #lista_people = list()
    print({"soy data"},datos.status_code)
    #"print("2")

    if datos.status_code == 200:
        content= datos.content
       # print(content)
        file = open('people.json','wb')
        file.write(content)
        file.close()
        #print(content)
    else:
        print("falla en requests")
    
    return("Almacenada api de personajes")  
    

@app.route('/api/postCharacter', methods=["POST"])  
def postCharacter():
    print("1")   
    url='./people.json'
    with open(url) as file:
     data = json.load(file)
     lista_person=list()
     print({"soy data"},data["results"])
     for personaje in data["results"]:

        character = Character()
        character.name = personaje['name']
        character.url = personaje['url']
        character.uid = personaje['uid']
        lista_person.append(character)
        db.session.add_all(lista_person)
        db.session.commit()
        characters = Character.query.all()
        characters=list(map(lambda character: character.serialize(), characters))
        file.close()
    return jsonify(characters), 200

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
    # SELECT * FROM users WHERE id = ?
    character = Character.query.get(id)

    # DELETE FROM users WHERE id=?
    character.delete()

    return jsonify({ "message": "Character Deleted" }), 202


 ##Funcion para salvar api de planetas desde la web y almacenar su info en archivo   
@app.route('/api/almacenaPlanetas', methods=["GET"])
def almacenaplanetas():
    #print("1")
    url ='https://www.swapi.tech/api/planets'

    datos = requests.get(url)
    #lista_people = list()
    print({"soy data"},datos.status_code)
    #"print("2")

    if datos.status_code == 200:
        content= datos.content
       # print(content)
        file = open('planets.json','wb')
        file.write(content)
        file.close()
        #print(content)
    else:
        print("falla en requests")
    
    return("Almacenada api de planetas")  
    

@app.route('/api/postPlanet', methods=["POST"])  
def postplanet():
    #print("1")   
    url='./planets.json'
    with open(url) as file:
     data = json.load(file)
     lista_planet=list()
     #print({"soy data"},data["results"])
     for planeta in data["results"]:

        planet = Planet()
        planet.name = planeta['name']
        planet.url = planeta['url']
        planet.uid = planeta['uid']
        lista_planet.append(planet)
        db.session.add_all(lista_planet)
        db.session.commit()
        planets = Planet.query.all()
        planets=list(map(lambda planet: planet.serialize(), planets))
        file.close()
    return jsonify(planets), 200

@app.route('/api/updatePlanet/<int:id>', methods=['PUT'])
def updateplanet(id):
    try:
        name = request.json.get('name') # None
        uid = request.json.get('id') # None
        url =  request.json.get('url') # None
    
        planet= Planet.query.get(id)
        planet.name = name
        planet.uid = id
        planet.url = url
        planet.update()

        return jsonify({"msg":"planeta actualizado"})
    except Exception as e:
        return jsonify({"msg":"planeta no actualizado"}),202
           
@app.route('/api/deletPlanet/<int:id>', methods=['DELETE'])
def deleteplanet(id):
    # SELECT * FROM users WHERE id = ?
    planet = Planet.query.get(id)

    # DELETE FROM users WHERE id=?
    planet.delete()

    return jsonify({ "message": "Planet Deleted" }), 202

##Funcion para salvar api de vehiculos desde la web y almacenar su info en archivo

@app.route('/api/almacenaVehiculos', methods=["GET"])
def almacenavehiculos():
    #print("1")
    url ='https://www.swapi.tech/api/vehicles'

    datos = requests.get(url)
    #lista_people = list()
    print({"soy data"},datos.status_code)
    #"print("2")

    if datos.status_code == 200:
        content= datos.content
       # print(content)
        file = open('vehicles.json','wb')
        file.write(content)
        file.close()
        #print(content)
    else:
        print("falla en requests")
    
    return("Almacenada api de Vehiculos")  
    

@app.route('/api/postVehicles', methods=["POST"])  
def postvehicles():
    #print("1")   
    url='./vehicles.json'
    with open(url) as file:
     data = json.load(file)
     lista_vehicles=list()
     #print({"soy data"},data["results"])
     for vehiculo in data["results"]:

        vehicle = Vehicle()
        vehicle.name = vehiculo['name']
        vehicle.url = vehiculo['url']
        vehicle.uid = vehiculo['uid']
        lista_vehicles.append(vehicle)
        db.session.add_all(lista_vehicles)
        db.session.commit()
        vehicles = Vehicle.query.all()
        vehicles=list(map(lambda vehicle: vehicle.serialize(), vehicles))
        file.close()
    return jsonify(vehicles), 200

@app.route('/api/updateVehicle/<int:id>', methods=['PUT'])
def updatevehicle(id):
    try:
        name = request.json.get('name') # None
        uid = request.json.get('id') # None
        url =  request.json.get('url') # None
    
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
    # SELECT * FROM users WHERE id = ?
    vehicle = Vehicle.query.get(id)

    # DELETE FROM users WHERE id=?
    vehicle.delete()

    return jsonify({ "message": "Vehicle Deleted" }), 202
    
       

#with app.app_context():
 #   db.create_all()

if __name__ == '__main__':
    app.run()