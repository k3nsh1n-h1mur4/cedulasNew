import os
from flask import Flask, render_template, url_for, flash, request
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2:///u?:p?@localhost:49262/?'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16)


db = SQLAlchemy(app)

class registroCedulas(db.Model):
    __tablename__ = '?'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), unique=False,  nullable=False)
    sexo = db.Column(db.String(20), unique=False, nullable=False)
    fnac = db.Column(db.String(10), unique=False, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    nss = db.Column(db.String(11), unique=True, nullable=False)
    rfc = db.Column(db.String(13), unique=True, nullable=False)
    curp = db.Column(db.String(18), unique=True, nullable=False)
    categoria = db.Column(db.String(100), unique=False, nullable=False)
    turno = db.Column(db.String(50), unique=False, nullable=False)
    tcontr = db.Column(db.String(20), unique=False, nullable=False)
    fingr = db.Column(db.String(10), unique=False, nullable=False)
    uadscripcion = db.Column(db.String(100), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Matrícula '{}' y Nombre: '{}'".format(self.matricula, self.nombrself.matricula, self.nombre)



@app.route('/')
def index():
    return 'Hola Mundo'


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        error = None
        matricula = request.form['matricula']
        nombre = request.form['nombre']
        sexo = request.form['sexo']
        fnac = request.form['fnac']
        correo = request.form['correo']
        telefono = request.form['telefono']
        nss = request.form['nss']
        rfc = request.form['rfc']
        curp = request.form['curp']
        categoria = request.form['categoria']
        turno = request.form['turno']
        tcontr = request.form['tcontr']
        fingr = request.form['fingr']
        uadscripcion = request.form['uadscripcion']

        
        cedula = registroCedulas(matricula=matricula, nombre=nombre, sexo=sexo, fnac=fnac, correo=correo, telefono=telefono, nss=nss, rfc=rfc, curp=curp, categoria=categoria, turno=turno, tcontr=tcontr, fingr=fingr, uadscripcion=uadscripcion)
        db.session.add(cedula)
        db.session.commit()
        db.session.close()



        flash(error)
    return render_template('registro.html')


    




if __name__ == '__main__':
    app.run()
