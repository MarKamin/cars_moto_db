
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy.sql import func


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars_and_moto_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("vardas", db.String(66))
    surname =db.Column("pavarde", db.String(66))
    email = db.Column("email", db.String(99), unique=True)
    telnr = db.Column("telnr", db.String(16))
    cars = db.relationship('Cars', backref='cars', lazy=True)
    motos = db.relationship('Moto', backref='moto', lazy=True)
    servisas = db.relationship("AutoTaisykla", backref="autoservisas", lazy=True)

    def __init__(self, name, surname, email, telnr):
        self.name = name
        self.surname = surname
        self.email = email
        self.telnr = telnr

class Cars(db.Model):
    __tablename__ = "Cars"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('Users.id'), nullable=False)
    cars_user = db.relationship("Users", backref="cars_users", lazy=True)
    servisas = db.relationship("AutoTaisykla", backref="Autoservisas", lazy=True)
    brand = db.Column("marke", db.String(66))
    model = db.Column("modelis", db.String(66))
    # year = db.Column("Metai", db.DateTime(datetime.date))
    year = db.Column("metai", db.String(4))
    rida = db.Column("rida", db.Float())
    kuras = db.Column("kuro_tipas", db.String(99))
    kebulas = db.Column("kebulas", db.String(99))
    kaina = db.Column("kaina", db.Float())
    vin_code = db.Column("vin_kodas", db.String(99))
    date_created = db.Column('sukurimo data', db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, brand, model, year, rida, kuras, kebulas, kaina, vin_code):
        self.user_id = user_id
        self.brand = brand
        self.model = model
        self.year = year
        self.rida = rida
        self.kuras = kuras
        self.kebulas = kebulas
        self.kaina = kaina
        self.vin_code = vin_code
        
class Moto(db.Model):
    __tablename__ = "Moto"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('Users.id'))
    motos_user = db.relationship("Users", backref="moto_users")
    brand = db.Column("marke", db.String(66))
    model = db.Column("modelis", db.String(66))
    tipas = db.Column('tipas', db.String(66))
    year = db.Column("metai", db.String(4))
    rida = db.Column('rida', db.Float())
    cc = db.Column("galingumas", db.Integer())
    kaina = db.Column("Kkaina", db.Float())
    svoris = db.Column("svoris", db.Float())
    date_created = db.Column('sukurimo data', db.DateTime(timezone=True), server_default=func.now())
    

    def __init__(self, user_id, brand, model, tipas, year, rida, cc, kaina, svoris):
        self.user_id = user_id
        self.brand = brand
        self.model = model
        self.tipas = tipas
        self.year = year
        self.rida = rida
        self.cc = cc
        self.kaina = kaina
        self.svoris = svoris

class AutoTaisykla(db.Model):
    __tablename__ = 'taisykla'
    id = db.Column('id', db.Integer, primary_key=True)
    auto_id = db.Column("cars_id", db.Integer, db.ForeignKey('Cars.id'), nullable=False)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('Users.id'), nullable=False)
    spec = db.Column('specializacja', db.String(55))
    pavadinimas = db.Column('pavadinimas', db.String(55))
    rating = db.Column('rating', db.Integer())
    date_created = db.Column('sukurimo data', db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, auto_id, user_id, pavadinimas, spec, rating):
        self.user_id = user_id
        self.auto_id = auto_id
        self.pavadinimas = pavadinimas
        self.spec = spec
        self.rating = rating
       
