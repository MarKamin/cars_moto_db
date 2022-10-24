from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import Users, app, db, Cars, Moto
from sqlalchemy.exc import IntegrityError

@app.route("/home")
def home():
    viso = Users.query.count()
    viso_auto= Cars.query.count()
    viso_moto= Moto.query.count()
    return render_template('home.html', viso=viso, viso_auto=viso_auto, viso_moto=viso_moto)

@app.route("/create_user", methods = ['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        try:
            vartotojas = Users(request.form['name'], request.form['surname'],
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

@app.route("/create_car", methods = ['GET', 'POST'])
def create_car():
    if request.method == 'POST':
        try:
            masina = Cars( request.form['user_id'], request.form['brand'],request.form['model'],request.form['year'], request.form['rida'],
        request.form['kuras'],request.form['kebulas'],request.form['kaina'],request.form['vin_code'])
            db.session.add(masina)
            db.session.commit()
            return '''<h1>Irasas sukurtas sekmingai</h1>
                        <a href="/home"> I pradzia </a> '''
        except ValueError:
            db.session.rollback()
            return '''<h1>Kazka ivedete netaip Perziurekite ir bandykite dar karta.</h1>
                      <a href="/create_user"> I pradzia </a> '''
    return render_template('create_car.html')

@app.route("/create_moto", methods = ['GET', 'POST'])
def create_moto():
    if request.method == 'POST':
        motoc = Moto( request.form['user_id'], request.form['brand'],request.form['model'],request.form['tipas'],request.form['year'],
    request.form['rida'],request.form['cc'],request.form['kaina'],request.form['svoris'])
        db.session.add(motoc)
        db.session.commit()
    return render_template('create_moto.html')

@app.route('/users_all')
def show_all_users():
    return render_template('users_all.html', users = Users.query.all() )

@app.route('/cars_all')
def show_all_cars():
    # expensive = db.session.execute(db.select(Cars).filter(Cars.kaina >= 5000)).all()
    return render_template('cars_all.html', cars = Cars.query.all())
    

@app.route('/cars_exp')
def cars_exp():
    expensive = db.session.execute(db.select(Cars.kaina, Cars.brand, Cars.user_id, Cars.id, 
    Cars.date_created, Cars.kebulas, Cars.kuras, Cars.model, Cars.year, Cars.rida, Cars.vin_code).filter(Cars.kaina >= 5000)).all()
    return render_template('cars_exp.html', users = Users.query.all(), expensive=expensive )

@app.route('/moto_all', methods = ['GET', 'POST'])
def show_all_moto():
    return render_template('moto_all.html', moto = Moto.query.all() )


@app.route('/delete_irasas_moto', methods = ['GET', 'POST'])
def delete_moto():
    id = request.form.get("moto_id")
    print(id)
    moto_trinamas = Moto.query.filter_by(id=id).first()
    print(type(moto_trinamas))
    print(moto_trinamas)
    db.session.delete(moto_trinamas)
    db.session.commit()
        
    return render_template('delete_irasas_moto.html')

@app.route('/delete_irasas_auto', methods = ['GET', 'POST'])
def delete_auto():
    id = request.form.get("car_id")
    print(id)
    auto_trinamas = Cars.query.filter_by(id=id).first()
    print(type(auto_trinamas))
    print(auto_trinamas)
    db.session.delete(auto_trinamas)
    db.session.commit()
        
    return render_template('delete_irasas_auto.html')

@app.route('/delete_irasas_user', methods = ['GET', 'POST'])
def delete_user():
    id = request.form.get("user_id")
    print(id)
    user_trinamas = Users.query.filter_by(id=id).first()
    print(type(user_trinamas))
    print(user_trinamas)
    db.session.delete(user_trinamas)
    db.session.commit()
        
    return render_template('delete_irasas_user.html')


with app.app_context():
    db.create_all()
    

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()