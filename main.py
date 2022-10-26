from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import Users, app, db, Cars, Moto, AutoTaisykla
from sqlalchemy.exc import IntegrityError, NoResultFound, StatementError
from sqlalchemy import select
from flask_sqlalchemy import record_queries



@app.route("/home")
def home():
    viso = Users.query.count()
    viso_auto= Cars.query.count()
    viso_moto= Moto.query.count()
    viso_serv = AutoTaisykla.query.count()
    return render_template('home.html', viso=viso, viso_auto=viso_auto, viso_moto=viso_moto, viso_serv=viso_serv)

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
            stmt = db.select(Users).where(Users.id == request.form['user_id']) # [? ? ? ?]
            print(type(stmt))
            user = db.session.scalars(stmt).one()
            # Scalar = Return the first element of the first result or None if no rows present. If multiple rows are returned, raises MultipleResultsFound.
            print(type(user))
            masina = Cars( user.id, request.form['brand'],request.form['model'],request.form['year'], request.form['rida'],
            request.form['kuras'],request.form['kebulas'],request.form['kaina'],request.form['vin_code'])
            db.session.add(masina)
            db.session.commit()
            return '''<h1>Irasas sukurtas sekmingai</h1>
                            <a href="/home"> I pradzia </a> 
                            <a href="/create_car"> Kurti kita irasa </a> '''
        except NoResultFound:
            return '<h1> Userio nera </h1>'
        except StatementError:
            db.session.rollback()
            return '''<h1>Kazka ivedete netaip Perziurekite ir bandykite dar karta.</h1>
                      <a href="/create_car"> I pradzia </a> '''
    return render_template('create_car.html')

@app.route("/create_moto", methods = ['GET', 'POST'])
def create_moto():
    if request.method == 'POST':
        motoc = Moto( request.form['user_id'], request.form['brand'],request.form['model'],request.form['tipas'],request.form['year'],
    request.form['rida'],request.form['cc'],request.form['kaina'],request.form['svoris'])
        db.session.add(motoc)
        db.session.commit()
    return render_template('create_moto.html')

@app.route("/create_service", methods = ['GET', 'POST'])
def create_service():
    if request.method == 'POST':
        try:
            stmt = db.select(Users).where(Users.id == request.form['user_id'])
            user = db.session.scalars(stmt).one()
            serv = AutoTaisykla( user.id, request.form['car_id'],request.form['name'], request.form['spec'], request.form['rating'] )
            db.session.add(serv)
            db.session.commit()
            return '''<h1>Serviso irasas sukurtas sekmingai</h1>
                            <a href="/home"> I pradzia </a> 
                            <a href="/create_service"> Kurti kita irasa </a> '''
        except NoResultFound:
            return '<h1> Userio nera </h1>'
        except StatementError:
            db.session.rollback()
            return '''<h1>Kazka ivedete netaip Perziurekite ir bandykite dar karta.</h1>
                      <a href="/create_service"> I pradzia </a> '''
    return render_template('create_service.html')

@app.route('/users_all')
def show_all_users():
    return render_template('users_all.html', users = Users.query.all() )

@app.route('/service_all')
def show_all_service():
    return render_template('service_all.html', taisykla = AutoTaisykla.query.all() )

@app.route('/cars_all')
def show_all_cars():
    # expensive = db.session.execute(db.select(Cars).filter(Cars.kaina >= 5000)).all()
    return render_template('cars_all.html', cars = Cars.query.all())
    

@app.route('/cars_exp')
def cars_exp():
    expensive = db.session.execute(db.select(Cars.kaina, Cars.brand, Cars.user_id, Cars.id,
    Cars.date_created, Cars.kebulas, Cars.kuras, Cars.model, Cars.year, Cars.rida, Cars.vin_code).filter(Cars.kaina >= 5000)).all()
    return render_template('cars_exp.html', expensive=expensive)

@app.route('/cars_cheap')
def cars_cheap():
    cheap = db.session.execute(db.select(Cars.kaina, Cars.brand, Cars.user_id, Cars.id, 
    Cars.date_created, Cars.kebulas, Cars.kuras, Cars.model, Cars.year, Cars.rida, Cars.vin_code).filter(Cars.kaina <= 5000)).all()
    return render_template('cars_cheap.html', cheap=cheap )

    # disel = session.execute(
    # select(Cars).where(Cars.kuras.like("%yzel%")).all

@app.route('/cars_diesel')
def cars_diesel():
    diesel = db.session.execute(db.select(Cars.kaina, Cars.brand, Cars.user_id, Cars.id, 
    Cars.date_created, Cars.kebulas, Cars.kuras, Cars.model, Cars.year, Cars.rida, Cars.vin_code).filter(Cars.kuras.like("%yzel%"))).all()
    # diesel = db.session.execute(db.select(Cars).where(Cars.kuras.like("%yzel%"))).all()
    # diesel = db.session.execute(db.select(Cars).filter(Cars.kuras.like("%yzel%"))).all()
    return render_template('cars_diesel.html', diesel=diesel)
    #db.select =  SQL executable arba 'construct'

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
    
######################## Kodas kad debugint sql queries ################
def sql_debug(response):
    queries = list(record_queries.get_recorded_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    print ('=' * 80)
    print (' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print ('=' * 80)
    print (query_str.rstrip('\n'))
    print ('=' * 80 + '\n')

    return response

if app.debug:
    app.after_request(sql_debug)
    

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()



