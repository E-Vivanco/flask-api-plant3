import os
from flask import Flask, request, jsonify, url_for, session,render_template
from flask_migrate import Migrate
#from flask_swagger import swagger
from flask_cors import CORS
#from utils import APIException, generate_sitemap
#from admin import setup_admin
from models import db,User,Character,Planet,Vehicle
import requests
import json
#from urllib import request
#from urllib.request import Request, urlopen
import sys
from flask_sqlalchemy import SQLAlchemy
#from flask_sqlalchemy import Model
from sqlalchemy import select, insert, create_engine
from sqlalchemy.sql import text
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

@app.route('/getCharacter', methods=["GET"])
def getCharacter():
    #print("1")
    url ='https://www.swapi.tech/api/people'

    datos = requests.get(url)
    lista_people = list()
    print({"soy data"},datos.status_code)
    #"print("2")

    if datos.status_code == 200:
        content= datos.content
       # print(content)
        file = open('people.json','wb')
        file.write(content)
        print(content)
    else:
        print("falla en requests")
        return ("Almacenada api de personajes")  

@app.route('/createCharacter', methods=["POST"])  
def createCharacter():
    print("1")   
    url='./people.json'
    with open(url) as file:
     data = json.load(file)
     print({"soy data"},data)
     for personaje in data["results"]:

        character = Character()
        character.name = personaje['name']
        character.url = personaje['url']
        #data2 = requests.get(personaje['url'])
       # print({"data2"},data2)
        character.uid = personaje['uid']
        character.save()
        file.close()
        return jsonify(character.serialize()), 201    

    #print("1")   
    #with open('people.json') as file:
    #    data = json.load(file)
    #    print(data["results"])
     #   for personaje in data["results"]:
     #       characters=Character()
     #       characters.name =personaje["name"]
     #       print(characters.name)
     #       characters.uid = personaje["uid"]
     #       print(characters.uid)
     #       characters.url = personaje["url"]
     #       data2 = requests.post(personaje['url'])
     #       print({"data2"},data2.serialize())
     #       lista_people.append(characters)
     #       print({"resultado"},Character.serialize(characters))
     #   file.close()
     #   db.session.add_all(lista_people)
     #   db.session.commit()
     #   #print({"soy characters"},characters)
    #return jsonify(Character.serialize(characters))
    #return ("Datos agregados a tabla Character")
    #print(response)  
   # for e in response["results"]:
   #     #print(e)
   #     characters=Character()
   #     print(e["name"])
   #     characters.name =e["name"]
   #     print(character.name)
   #     characters.uid = e["uid"]
   #     characters.url=e["url"]
   # list_people.append(characters)
    #print()
    #db.save()
   # db.session.add(list_people)
    #db.session.commit()
    

    #y='https://www.swapi.tech/api/planets'
    #z='https://www.swapi.tech/api/vehicles' 
   # print("El commit")
    #print(jsonify(list_planets))
   # response1 =requests.get(y)
   # response2 = requests.get(z)
   # if response.status_code == 200:
   #     content = response.content
   #     file = open('people.json','wb')
   #     file.write(content)
   #     file.close()
   # if response1.status_code == 200:
   #     content2= response1.content
   #     file = open('planets.json','wb')
   #     file.write(content2)
   #     file.close()
   # if response2.status_code == 200:
   #     content3= response2.content
   #     file = open('vehicles.json','wb')
   #     file.write(content3)
   #     file.close()

    
    
    

#with app.app_context():
 #   db.create_all()

if __name__ == '__main__':
    app.run()