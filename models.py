
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from sqlalchemy.sql import func


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auto_moto_DB.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFIACTIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("vardas", db.String(66))
    surname =db.Column("pavarde", db.String(66))
    email = db.Column("email", db.String(99), unique=True)
    telnr = db.Column("telnr", db.String(16))
    
    def __init__(self, name, surname, email, telnr):
        self.name = name
        self.surname = surname
        self.email = email
        self.telnr = telnr

class cars(db.Model):
    __tablename__ = "cars"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'))
    car_user = db.relationship("users", backref=db.backref("moto_users", uselist=False))
    brand = db.Column("Marke", db.String(66))
    model = db.Column("Modelis", db.String(66))
    # year = db.Column("Metai", db.DateTime(datetime.date))
    year = db.Column("Metai", db.String(4))
    kuras = db.Column("Kuro_tipas", db.String(99))
    kebulas = db.Column("Kebulas", db.String(99))
    kaina = db.Column("Kaina(€)", db.Float())
    vin_code = db.Column("VIN_kodas", db.String(99))
    date_created = db.Column('Sukurimo data', db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, user_id, brand, model, year, kuras, kebulas, kaina, vin_code):
        self.user_id = user_id
        self.brand = brand
        self.model = model
        self.year = year
        self.kuras = kuras
        self.kebulas = kebulas
        self.kaina = kaina
        self.vin_code = vin_code
        
class moto(db.Model):
    __tablename__ = "moto"
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'))
    moto_user = db.relationship("users", backref=db.backref("users", uselist=False))
    brand = db.Column("Marke", db.String(66))
    model = db.Column("Modelis", db.String(66))
    tipas = db.Column('Tipas', db.String(66))
    year = db.Column("Metai", db.String(4))
    cc = db.Column("Galingumas", db.Integer())
    kaina = db.Column("Kaina(€)", db.Float())
    svoris = db.Column("Svoris", db.Float())
    date_created = db.Column('Sukurimo data', db.DateTime(timezone=True), server_default=func.now())
    

    def __init__(self, user_id, brand, model, tipas, year, cc, kaina, svoris):
        self.user_id = user_id
        self.brand = brand
        self.model = model
        self.tipas = tipas
        self.year = year
        self.cc = cc
        self.kaina = kaina
        self.svoris = svoris
       
