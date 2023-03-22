from flask_sqlalchemy import SQLAlchemy
db= SQLAlchemy()

class User(db.Model):
    __tablaname__='users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    isActive = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "isActive": self.isActive
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
    __tablaname__='characters'
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
    __tablaname__='planets'
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
    __tablaname__='vehicles'
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
