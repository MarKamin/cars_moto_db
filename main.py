from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import users, app, db, cars, moto
from sqlalchemy.exc import IntegrityError

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/create_user", methods = ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        try:
            vartotojas = users(request.form['name'], request.form['surname'],
            request.form['email'], request.form['telnr'])
            db.session.add(vartotojas)
            db.session.commit()
            return '''<h1>Vartotojas sukurtas sekmingai</h1>
                      <a href="/home"> I pradzia </a> '''
        except IntegrityError:
            db.session.rollback()
            return '''<h1>Jau Egsistuoja. Sugalvokite kita emaila</h1>
                      <a href="/create_user"> I pradzia </a> '''
        
    return render_template('create_user.html')

@app.route("/create_car")
def create_car():
    pass

@app.route("/create_moto")
def create_moto():
    pass

@app.route('/users_all')
def show_all_users():
    pass

@app.route('/cars_all')
def show_all_cars():
    pass

@app.route('/moto_all')
def show_all_moto():
    pass

with app.app_context():
    db.create_all()
    

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()