from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=False,nullable=False)
    lastname = db.Column(db.String(100),unique=False,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favoritos=db.relationship('Favorito',cascade="all,delete",secondary="favoritosall",back_populates="users")
    #favoritos=db.relationship('Character',secondary=favoritosall,backref=db.backref('users',lazy=True))
    #favoritos=db.relationship('Vehicle',secondary=favoritosall,backref=db.backref('users',lazy=True))

    
    #def __repr__(self):
    #    return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "lastname": self.lastname,
            "email": self.email,
            #"password":self.password
            #"isActive": self.isActive
            # do not serialize the password, its a security breach
        }
    def save(self):
        db.session.add_all(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Character(db.Model):
    __tablename__='character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    url = db.Column(db.String(100), unique=False, nullable=False)
    uid = db.Column(db.String(100), unique=False, nullable=False)


    def serialize(self):
        return{
            "name":self.name,
            "url":self.url,
            "uid":self.uid,
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Planet(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    url = db.Column(db.String(100), unique=False, nullable=False)
    uid = db.Column(db.String(100), unique=False, nullable=False)

    def serialize(self):
        return{
            "name":self.name,
            "url":self.url,
            "uid":self.uid,
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Vehicle(db.Model):
    __tablename__='vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    url = db.Column(db.String(100), unique=False, nullable=False)
    uid = db.Column(db.String(100), unique=False, nullable=False)
    def serialize(self):
        return{
            "name":self.name,
            "url":self.url,
            "uid":self.uid,
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

class Favorito(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    users = db.relationship('User',cascade="all,delete",secondary="favoritosall")
    planets = db.relationship('Planet',cascade="all,delete",secondary="favoritosall")
    character = db.relationship('Character',cascade="all,delete",secondary="favoritosall")
    vehicles = db.relationship('Vehicle',cascade="all,delete",secondary="favoritosall")

    def serialize(self):
        return{
            "id":self.id,
            "name":self.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
        
    def get_favoritos(self):
        return list(map(lambda favorito: favorito.serialize(),self.favoritos))


class Favoritosall(db.Model):
     __tablename__='favoritosall'
     favorito_id= db.Column(db.Integer,db.ForeignKey('favoritos.id',ondelete='CASCADE'),primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
     character_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
     planet_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
     vehicle_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
#

#class FavoritosPlanetas(db.Model):
#    __tablaname__='favoritosplanetas'
#    db.Column('user_id',db.Integer,db.ForeignKey('user.id'), primary_key=True),
#    db.Column('planet_id',db.Integer,db.ForeignKey('planet.id'), primary_key=True)
#
#class FavoritosPersonajes(db.Model):
#    __tablaname__='favoritospersonajes'
#    db.Column('user_id',db.Integer,db.ForeignKey('user.id'), primary_key=True),
#    db.Column('character_id',db.Integer,db.ForeignKey('character.id'), primary_key=True)
##
#class FavoritosVehiculos(db.Model):
#    __tablaname__='favoritosvehiculos'
#    db.Column('user_id',db.Integer,db.ForeignKey('user.id'), primary_key=True),
#    db.Column('vehicle_id',db.Integer,db.ForeignKey('vehicle.id'), primary_key=True)
#

