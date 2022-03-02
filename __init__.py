import os
from flask import Flask, render_template, url_for, flash, request, g, flash, redirect, abort
import sqlite3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import requests



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2:///u?:p?@localhost:49262/?'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16)


shell = app.make_shell_context()
shell['name'] = app

db = SQLAlchemy(app)

class registroCedulas(db.Model):
    __tablename__ = 'cedulasTable'

    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100),  nullable=False)
    sexo = db.Column(db.String(20), nullable=False)
    fnac = db.Column(db.String(10), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    nss = db.Column(db.String(11), nullable=False)
    rfc = db.Column(db.String(13), nullable=False)
    curp = db.Column(db.String(18), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    turno = db.Column(db.String(50), nullable=False)
    tcontr = db.Column(db.String(20), nullable=False)
    fingr = db.Column(db.String(10), nullable=False)
    uadscripcion = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def verify_matricula(matricula):
        matricula = registroCedulas.query.filter_by(matricula=matricula).first()
        return matricula

    @classmethod
    def get_matricula(cls, matricula):
        return registroCedulas.query.filter_by(matricula=matricula).first()

    def __repr__(self):
        return "Matrícula '{}' y Nombre: '{}'".format(self.matricula, self.nombre)


#decorador
#a(b)-> c
#A recibe como parametro B para poder crear C
def my_decorator(function):
    def wrapper(*args, **kwargs):
        print("hola warpper")
        con = sqlite3.connect("")
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        rows = cursor.execute('SELECT * FROM ... WHERE matricula={}'.format(...))
        result = rows.fetchone()
        print(result[1])
        
        
        return function(*args, **kwargs)
        print("cerrando conexion")
        con.close()
    return wrapper
 

@app.route('/')
def index():
    print(dir(g))
    return render_template('errors.html')


@app.errorhandler(404)
def errors_sqlite(error):
    return render_template('errors.html'), 404



@app.route('/validate_matricula', methods=['GET', 'POST'])
def validate_matricula():
    error = None
    if request.method == 'GET':
        matricula = request.args.get('matricula')
        mat = registroCedulas.query.filter_by(matricula=matricula).first()
        if mat:
            flash('Matrícula ya registrada')
            return render_template('errors/matricula.html', error=error)
        elif mat is None:
            print('hola')
            return render_template('validate_matricula.html', mat=mat, title='Verifica Matrícula')
       
        #print(mat)
    #return render_template('validate_matricula.html')
    
   
@app.route('/registro', methods=['GET', 'POST'])
#@my_decorator
def registro():
    try:
        if request.method == 'POST':
            mat = None
            print(request.headers)
            mat = registroCedulas.query.filter_by(matricula=request.form['matricula']).first()
            print(mat)
                
            matricula = request.form['matricula']  
            if mat == matricula:
                flash("matricula ya registrada")
                return render_template('errors/matricula.html')      

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

            """if not matricula:
                error = 'Campo Vacío'
            elif not nombre:
                error = 'Campo Vacío'"""

                
            cedula = registroCedulas(matricula=matricula, nombre=nombre.upper(), sexo=sexo.upper(), fnac=fnac, correo=correo, telefono=telefono, nss=nss, rfc=rfc.upper(), curp=curp.upper(), categoria=categoria.upper(), turno=turno, tcontr=tcontr, fingr=fingr, uadscripcion=uadscripcion.upper())
            db.session.add(cedula)
            db.session.commit()
            db.session.close()
        
    except sqlite3.IntegrityError:
            print("matricula ya registrada")
         
       # flash(error)
    return render_template('registro.html', 
            cat = [
                {"categoria": "Pasante de Abogado"}, {"categoria": "Abogado"}, {"categoria": "Auxiliar Técnico de Actuariado Social"}, {"categoria": "Oficial Técnico de Actuariado Social"}, 
                {"categoria": "Técnico de Actuariado Social"}, {"categoria": "Actuario Social Matemático"}, {"categoria": "Auxiliar de Almacen"}, {"categoria":"Oficial de Almacén"}, 
                {"categoria":"Coordinador de Almacén"}, {"categoria":"Jefe de Grupo de Almacén"}, {"categoria":"Especialista de Almacén"}, {"categoria":"Arquitecto"},
                {"categoria":"Asistente Medica"}, {"categoria": "Coordinadora de Asistente Medica"}, {"categoria":"Ayudante de Autopsias"}, {"categoria":"Auxiliar de Servicios Administrativos"},
                {"categoria":"Tecnico de Bibliotecas"}, {"categoria":"Asistente de Bibliotecario"}, {"categoria": "Bibliotecario"}, {"categoria":"Tecnico de Bibliotecas"}, {"categoria":"Asistente de Bibliotecario"}, 
                {"categoria": "Bibliotecario"},
                {"categoria":"Ayudante de Cajero B"}, {"categoria":"Ayudante de Cajero A"}, {"categoria":"Cajero D"}, {"categoria":"Cajero C"}, {"categoria":"Cajero B"}, {"categoria":"Cajero A"}, 
                {"categoria":"Camillero de Unidades Medicas"}, {"categoria": "Auxiliar de Administracion de C.V."}, {"categoria": "Auxiliar de Atencion Medica ccd C.V."}, {"categoria": "Auxiliar de Hospedaje de C.V."}, 
                {"categoria": "Auxiliar de Operacion Contable de C.V."}, {"categoria":"Lavandero en Centros Vacacionales"}, {"categoria":"Operador de Seguridad en Albercas de C.V."}, {"categoria":"Operador de Servicios Internos de C.V."}, 
                {"categoria":"Operador de Vehiculos de C.V."}, {"categoria":"Planchador de Centros Vacacionales"}, {"categoria":"Vigilante de Centros Vacacionales"}, {"categoria":"Cirujano Maxilo Facal"}, 
                {"categoria":"Citotecnologo"}, {"categoria":"Tecnico Polivalente"},{"categoria":"Tecnico Electrisista"}, {"categoria":"Tecnico Electronico"},{"categoria":"Tecnico Mecanico"},{"categoria":"Tecnico Plomero"},
                {"categoria":"Tecnico A en Aire Acondicionado y Refrigeracion"}, {"categoria":"Tecnico A en Equipos Medicos"},{"categoria":"Tecnico A en Fluidos y Energeticos"},{"categoria":"Tecnico A en Plantas de Lavado"},
                {"categoria":"Tecnico A en Telecomunicaciones"},
                {"categoria":"Tecnico B en Equipos Medicos"},{"categoria":"Tecnico B en Fluidos y Energeticos"},{"categoria":"Tecnico B en Planta de Lavado"},{"categoria":"Tecnico B en Telecomunicaciones"},
                {"categoria":"Tecnico en Equipos Reciprocantes"},{"categoria":"Tecnico en Electronica Medica y Laboratorio"},{"categoria":"Tecnico C en Fluidos y Energeticos"},{"categoria":"Tecnico C en Plantas de Lavado"},
                {"categoria":"Tecnico C en Telecomunicaciones"},{"categoria":"Tecnico en Mecanica, Fluidos y Especialidades"},{"categoria":"Tecnico en Equipos de Absorcion"},{"categoria":"Tecnico en Equipos Helicoidal"},
                {"categoria":"Tecnico en Equipo de Rayos X"},{"categoria":"Tecnico en Equipos Turbocentrifugo"},{"categoria":"Especialista en Equipo de Especialidades"},{"categoria":"Especialista en Equipos de Laboratorio"},
                {"categoria":"Especialista en Equipos de Medica y Fluidos"},{"categoria":"Especialista en Equipos de Aire Acondicionado y Refrigeracion"},{"categoria":"Especialista en Plantas de Lavado"},
                {"categoria":"Especialista en Equipos de Electronica Medica"},{"categoria":"Especialista en Equipos de Rayos X"},{"categoria":"Especialista en Fluidos y Energeticos"}, {"categoria":"Contador"}, 
                {"categoria":"Contador Auditor"},
                {"categoria":"Cuidador de Animales"}, {"categoria":"Dibujante de Construccion"}, {"categoria":"Dibujante de Estadistica y Publicidad C"},{"categoria":"Dibujante de Estadistica y Publicidad B"},
                {"categoria":"Dibujante de Estadistica y Publicidad A"},{"categoria":"Dibujante de Ingenieria y Arquitectura"}, {"categoria":"Pasante de Economista"}, {"categoria":"Economista"}, {"categoria":"Educadora"},
                {"categoria":"Electrocardiografista"}, {"categoria":"Elevadorista"}, {"categoria":"Auxiliar de Enfermeria General"},{"categoria":"Auxiliar de Enfermeria en Salud Publica"},{"categoria":"Enfermera General"},
                {"categoria":"Enfermera Especialista"},{"categoria":"Enfermera Jefe de Piso"}, {"categoria":"Estomatologo"}, {"categoria":"Auxiliar de Farmacia"}, {"categoria":"Ayudante de Farmacia"}, {"categoria":"Oficial de Farmacia"}, 
                {"categoria":"Coordinador de Farmacia"}, {"categoria":"Fonoaudiologo"}, {"categoria":"Guardavidas"}, {"categoria":"Oficial de Puericultura"}, {"categoria":"Tecnico de Puericultura"}, 
                {"categoria":"Heliografista"}, {"categoria":"Histotecnologo"}, {"categoria":"Pasante de Ingeniero"}, {"categoria":"Ingeniero"}, {"categoria":"Inhaloterapia"}, {"categoria":"Auxiliar de Servicios de Intendencia"}, 
                {"categoria":"Ayudante de Servicios de Intendencia"}, {"categoria":"Oficial Servicio de Intendencia"}, {"categoria":"Intendente"}, {"categoria":"Auxiliar de Laboratorio"}, {"categoria":"Laboratorista"},
                {"categoria":"Operador de Servicios de Lavanderia"}, {"categoria":"Oficial de Servicios de Lavanderia"}, {"categoria":"Auxiliar de Limpieza e Higiene en Unidades Medicas y No Medicas"}, 
                {"categoria":"Ayudante de Limpieza e Higiene en Unidades Medicas y No Medicas"}, {"categoria":"Machetero"}, {"categoria":"Masajista"}, {"categoria":"Medico General"}, 
                {"categoria":"Medico No Familiar"}, {"categoria":"Medico Familiar"},
                {"categoria":"Tecnico de Microfotografia"}, {"categoria":"Multilitista"}, {"categoria":"Nutricion Dietista"}, {"categoria":"Especialista en Nutricion y Dietetica"}, {"categoria":"Nutriologo Clinico Especializado"},
                {"categoria":"Operador de Maquinas de Revelado Automatico"}, {"categoria":"Operador de Maquinas de Revelado Automatico"}, {"categoria":"Optometrista"}, {"categoria":"Orientador"}, 
                {"categoria":"Orientadoe de Actividades Familiares"}, {"categoria":"Orientador de Actividades Artisticas"}, {"categoria":"Orientador de Actividades Artisticas Danza Regional"}, 
                {"categoria":"Orientador de Actividades Artisticas Maestro de Musical"}, {"categoria":"Orientador de Actividades Artisticas Arte Dramatico"}, {"categoria":"Orientador de Educacion Fisica"},
                {"categoria":"Orientador de Iniciacion Cultural"}, {"categoria":"Orientador Tecnico Medico"},                
                {"categoria":"Auxiliar de Orientador Tecnico Medico"}, {"categoria":"Ortopedista"}, {"categoria":"Partera"}, {"categoria":"Jefe de Parteras"}, {"categoria":"Peluquero"}, {"categoria":"Pianista"},
                {"categoria":"Auxiliar de Administracion en Unidad Medica"},{"categoria":"Auxiliar de Enfermeria en Unidad Medica"}, {"categoria":"Auxiliar de Limpieza y Cocina en Unidad Medica"}, 
                {"categoria":"Auxiliar de Servicios Generales en Unidad Medica"}, {"categoria":"Profesor de Educacion Fisica A"}, {"categoria":"Profesor de Educacion Fisica B"}, {"categoria":"Profesor de Educacion Fisica C"},
                {"categoria":"Promotor de Estomatologia"}, {"categoria":"Promotor de Salud Comunitaria"}, {"categoria":"Psicologo"}, {"categoria":"Psicolog Clinico"}, {"categoria":"Psicometra"}, 
                {"categoria":"Quimico Clinico"}, {"categoria":"Quimico Clinico Jefe de Seccion"}, {"categoria":"Tecnico Radiologo"}, {"categoria":"Radioterapeuta"}, {"categoria":"Redactor B"},
                {"categoria":"Auxiliar de Administracion en Unidad Medica"}, {"categoria":"Auxiliar de Enfermeria en Unidad Medica"}, {"categoria":"Auxiliar de Limpieza y Cocina en Unidad Medica"},
                {"categoria":"Auxiliar de Servicios Generales en Unidad Medica"},
                {"categoria":"Sociologo"}, {"categoria":"Auxiliar de Soporte Tecnico en Informatica"}, {"categoria":"Oficial Soporte Tecnico en Informatica"}, {"categoria":"Coordinador de Soporte Tecnico en Informatica"},
                {"categoria":"Tecnico en Anestesia"}, {"categoria":"Tecnico en el manejo de Aparatos de Electrodiagnostico"}, {"categoria":"Tecnico en Medicina Nuclear"}, {"categoria":"Auxiliar de Tecnico en Servicios de Dietologia"},
                {"categoria":"Operador Telefonico A"}, {"categoria":"Operador Telefonico B"}, {"categoria":"Operador Telefonico C"}, {"categoria":"Coordinador de Operadores Telefonicos"}, {"categoria":"Terapista Fisico"}, 
                {"categoria":"Terapista Ocupacional"},
                {"categoria":"Operador General de Tiendas"}, {"categoria":"Jefe de Linea en Tiendas"}, {"categoria":"Trabajador Social"}, {"categoria":"Trabajador Social Clinico"}, {"categoria":"Auxiliar de Trabajo Social"},
                {"categoria":"Chofer"}, {"categoria":"Motociclista"}, {"categoria":"Controlador de Vehiculos"}, {"categoria":"Enfermera para el Traslado de Pacientes de Urgencia"}, 
                {"categoria":"Enfermera para el Traslado de Pacientes de Terapia Intensiva"},
                {"categoria":"Tecnico Operador de Transporte de Pacientes de Urgencia"},{"categoria":"Tecnico Operador de Transporte de Pacientes de Terapia Intensiva"},{"categoria":"Medico para el Traslado de Pacientes de Urgencia"},
                {"categoria":"Medico para el Traslado de Pacientes de Terapia Intensiva"}, {"categoria":"Auxiliar de Administracion en Unidad Medica de Esquema Modificado y Campo"},
                {"categoria":"Auxiliar de Atencion Medica en Unidad Medica de Esquema Modificado"},{"categoria":"Auxiliar de Laboratorio en Unidad Medica de Esquema Modificado y Campo"},
                {"categoria":"Auxiliar de Servicios Generales en Unidad Medica de Esquema Modificado y Campo"}, {"categoria":"Estomatologo en Unidad Medica de Esquema Modificado y Campo"},
                {"categoria":"Operador de Servicios de Radiodiagnostico en Unidad Medica de Esquema Modificado y Campo"}, {"categoria":"Auxiliar de Administracion en Unidad Medica de Esquema Modificado de Campo"},
                {"categoria":"Auxiliar de Area Medica en Unidad Medica de Campo"},{"categoria":"Auxiliar de Servicios Generales en Unidad Medica de  Campo"}, {"categoria":"Estomatologo en Unidad Medica de Campo Campo"},
                {"categoria":"Operador de Mantenimiento en Unidad Medica de Campo"}, {"categoria":"Operador de Servicios Auxiliares en Unidad Medica de Campo laboratorio"}, 
                {"categoria":"Operador de Servicios Auxiliares en Unidad Medica de Campo Radiodiagnostico"}, {"categoria":"Mensajero"}, {"categoria":"Auxiliar Universal de Oficinas"}, 
                {"categoria":"Oficial de Tesoreria"}, {"categoria":"Coordinador de Tesoreria"}, {"categoria":"Jefe de Grupo de Tesoreria"}, {"categoria":"Especialista de Tesoreria"},
                {"categoria":"Oficial de Servicios Tecnicos"},{"categoria":"Coordinador de Servicios Tecnicos"},{"categoria":"Jefe de Grupo de Servicios Tecnicos"},{"categoria":"Especialista de Servicios Tecnicos"},
                {"categoria":"Oficial de Servicios Administrativos"},{"categoria":"Coordinador de Servicios Administrativos"},{"categoria":"Jefe de Grupo de Servicios Administrativos"},{"categoria":"Especialista de Servicios Administrativos"},
                {"categoria":"Oficial de Personal"},{"categoria":"Coordinador de Personal"},{"categoria":"Jefe de Grupo de Personal"},{"categoria":"Especialista de Personal"},
                {"categoria":"Oficial de Estadistica"},{"categoria":"Coordinador de Estadistica"},{"categoria":"Jefe de Grupo Estadistica"},{"categoria":"Especialista de Estadistica"},
                {"categoria":"Oficial de Procesameinto de Datos"},{"categoria":"Coordinador de Procesamiento de Datos"},{"categoria":"Jefe de Grupo de Procesamiento de Datos"},{"categoria":"Especialista de Procesamiento de Datos"},
                {"categoria":"Oficial de Contabilidad"},{"categoria":"Coordinador de Contabilidad"},{"categoria":"Jefe de Grupo de Contabilidad"},{"categoria":"Especialista de Contabilidad"},
                {"categoria":"Jefe de Oficina A"},{"categoria":"Jefe Tecnico de Cobranza y Adeudos"},{"categoria":"Jefe de Grupo de Servicios de Personal"},
                {"categoria":"Camillero de Vehiculos de Servicios Ordinarios y Programados"},{"categoria":"Operador de Vehiculos de Servicios Ordinarios y Programados"},{"categoria":"Operador de Ambulancias"},
                {"categoria":"Controlador de Vehiculos de Servicios Ordinarios y Programados"}, {"categoria":"Auxiliar de Velatorio"},{"categoria":"Operador de Velatorio"},{"categoria":"Ayudante de Embalsamiento"},
                {"categoria":"Veterinario"}, {"categoria":"Yesista"},],

        

        turno = [{'turno': 'Matutino'}, {'turno': 'Vespertino'}, {'turno': 'Nocturno'}, {'turno': 'Jornada Acumulada'}],
        cont = [{'contratacion': '02 Base'}, {'contratacion': '08 Eventual'}, {'contratacion': 'Confianza B'}, {'contratacion': '03 Temporal'}],
        adscripciones = [
                        {'adscripcion': 'BANCO DE SANGRE'}, 
                        {'adscripcion': 'CAO'},
                        {'adscripcion': 'CENTRAL DE SERVICIOS'},
                        {'adscripcion': 'CENTRO DE CANJE'},
                        {'adscripcion': 'CENTRO DE SIMULACION'},
                        {'adscripcion': 'CIBO'},
                        {'adscripcion': 'CLINICA DE MAMA'},
                        {'adscripcion': 'DELEGACION JALISCO'},
                        {'adscripcion': 'HOSPITAL ESPECIALIDADES'},
                        {'adscripcion': 'HOSPITAL GINECO-OBSTETRICIA'},
                        {'adscripcion': 'HOSPITAL PEDIATRIA'},
                        {'adscripcion': 'PATOLOGIA CLINICA'},
                        {'adscripcion': 'PLANTA CENTRAL DE LAVADO'},
                        {'adscripcion': 'TELECOMUNICACIONES'},
                        {'adscripcion': 'TIENDA CENTRO MEDICO'},
                        {'adscripcion': 'TRANSPORTES'},
                        {'adscripcion': 'UMF 003'},
                        {'adscripcion': 'HGZ 014'},
                        {'adscripcion': 'UMF 049'},
                        {'adscripcion': 'UMF 052'},
                        {'adscripcion': 'UMF 054'},
                        {'adscripcion': 'UMF 078'},
                        {'adscripcion': 'UMF 093'},
                        {'adscripcion': 'UMF 167'},
                        {'adscripcion': 'UMF 184'},
                        {'adscripcion': 'CENTRO COMUNITARIO DE SALUD MENTAL'},
                        {'adscripcion': 'HGR 045'},
                        {'adscripcion': 'HOSPITAL JUAN I. MENCHACA'},
                        {'adscripcion': 'LARRE'},
                        {'adscripcion': 'UMF 002'},
                        {'adscripcion': 'UMF 004'},
                        {'adscripcion': 'UMF 008'},
                        {'adscripcion': 'UMF 051'},
                        {'adscripcion': 'UMF 053'},
                        {'adscripcion': 'UMF 079'},
                        {'adscripcion': 'UMF 182'},
                        {'adscripcion': 'ALMACEN DELEGACIONAL'},
                        {'adscripcion': 'CENTRO DE SEGURIDAD SOCIAL GUADALAJARA'},
                        {'adscripcion': 'HGR 046'},
                        {'adscripcion': 'TIENDA CAMPESINO'},
                        {'adscripcion': 'UMF 001'},
                        {'adscripcion': 'UMF 034'},
                        {'adscripcion': 'UMF 039'},
                        {'adscripcion': 'UMF 088'},
                        {'adscripcion': 'UMF 091'},
                        {'adscripcion': 'UMF 092'},
                        {'adscripcion': 'HGZ 089'},
                        {'adscripcion': 'UMF 055'},
                        {'adscripcion': 'UMF 171'},
                        {'adscripcion': 'UMF 178'},
                        {'adscripcion': 'VELATORIO'},
                        {'adscripcion': 'HGR 110'},
                        {'adscripcion': 'UMF 048'},
                        {'adscripcion': 'HGR 180'},
                        {'adscripcion': 'UMF 059'},
                        {'adscripcion': 'CENTRO DE CAPACITACION Y CALIDAD JALISCO'},
                        {'adscripcion': 'GUARDERIA 01'},
                        {'adscripcion': 'GUARDERIA 02'},
                        {'adscripcion': 'GUARDERIA 03'},
                        {'adscripcion': 'GUARDERIA 04'},
                        {'adscripcion': 'GUARDERIA 05'},
                        {'adscripcion': 'SUBDELEGACION REFORMA LIBERTAD'},
                        {'adscripcion': 'SUBDELEGACION JUAREZ'},
                        {'adscripcion': 'SUBDELEGACION HIDALGO'},
                        {'adscripcion': 'ESCUELA DE ENFERMERIA'},
                        {'adscripcion': 'HGZ 020 AUTLAN DE NAVARRO'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 125 EL LIMON'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 127 TONAYA'},
                        {'adscripcion': 'UMF 071 AYUTLA'},
                        {'adscripcion': 'UMF 081 EL GRULLO'},
                        {'adscripcion': 'HGsZ 028 CASIMIRO CASTILLO'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 122 CUATITLAN'},
                        {'adscripcion': 'UMF 070 CAREYES'},
                        {'adscripcion': 'UMF 080 CIHUATLAN'},
                        {'adscripcion': 'UMF 083 LA HUERTA'},
                        {'adscripcion': 'UMF 162 MELAQUE'},
                        {'adscripcion': 'CENTRO DE SEGURIDAD SOCIAL CD. GUZMAN'},
                        {'adscripcion': 'HGsZ 015 TAMAZULA'},
                        {'adscripcion': 'HGZ 009 CD. GUZMAN'},
                        {'adscripcion': 'OFNA AUX 120'},
                        {'adscripcion': 'OFNA AUX 150'},
                        {'adscripcion': 'PUESTO ENFERMERIA 180 TOLIMAN'},
                        {'adscripcion': 'SUBDELEGACION CD. GUZMAN'},
                        {'adscripcion': 'TIENDA CD. GUZMAN'},
                        {'adscripcion': 'UMF 013 PIHUAMO'},
                        {'adscripcion': 'UMF 016 TECALITLAN'},
                        {'adscripcion': 'UMF 017 ATENQUIQUE'},
                        {'adscripcion': 'UMF 018 ZAPOTILTIC'},
                        {'adscripcion': 'UMF 019 TUXPAN'},
                        {'adscripcion': 'UMF 033 SAN MARCOS'},
                        {'adscripcion': 'UMF 035 VISTA HERMOSA'},
                        {'adscripcion': 'UMF 036 LA GARITA'},
                        {'adscripcion': 'UMF 061 MAZAMITLA'},
                        {'adscripcion': 'UMF 062 SAYULA'},
                        {'adscripcion': 'UMF 063 SAN GABRIEL'},
                        {'adscripcion': 'UMF 064 TAPALPA'},
                        {'adscripcion': 'UMF 065 TECHALUTA'},
                        {'adscripcion': 'UMF 076 TEOCUITATLAN'},
                        {'adscripcion': 'UMF 114 GOMEZ FARIAS'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 155 TIZAPAN'},
                        {'adscripcion': 'UMF 005 EL SALTO'},
                        {'adscripcion': 'UMF 040 CHAPALA'},
                        {'adscripcion': 'UMF 047 ZAPOTLANEJO'},
                        {'adscripcion': 'UMF 057 iXTLAHUACAN DEL RIO'},
                        {'adscripcion': 'UMF 058 JOCOTEPEC'},
                        {'adscripcion': 'UMF 060 COLOTLAN'},
                        {'adscripcion': 'UMF 068 BOLAÑOS'},
                        {'adscripcion': 'UMF 106 SAN MARTIN BOLAÑOS'},
                        {'adscripcion': 'UMF 181 IXTLAHUACAN DE LOS MEMBRILLOS'},
                        {'adscripcion': 'CENTRO DE SEGURIDAD LAGOS DE MORENO'},
                        {'adscripcion': 'HGZ 007 LAGOS DE MORENO'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 130 OJUELOS'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 133 UNION DE SAN ANTONIO'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 135 VILLA HIDALGO'},
                        {'adscripcion': 'SUBDELEGACION LAGOS DE MORENO'},
                        {'adscripcion': 'UMF 041 SAN JUAN DE LOS LAGOS'},
                        {'adscripcion': 'UMF 084 ENCARNACION DE DIAZ'},
                        {'adscripcion': 'UMF 087 TEOCALTICHE'},
                        {'adscripcion': 'UMF 131 SAN DIEGO DE ALEJANDRIA'},
                        {'adscripcion': 'UMF 177 LAGOS DE MORENO'},
                        {'adscripcion': 'CENTRO DE SEGURIDAD SOCIAL OCOTLAN'},
                        {'adscripcion': 'HGZ 006 OCOTLAN'},
                        {'adscripcion': 'SUBDELEGACION OCOTLAN'},
                        {'adscripcion': 'UMF 022 ATOTONILCO'},
                        {'adscripcion': 'UMF 023 LA BARCA'},
                        {'adscripcion': 'UMF 050 ATOTONILQUILLO'},
                        {'adscripcion': 'UMF 066 AYOTLAN'},
                        {'adscripcion': 'UMF 067 TOTOTLAN'},
                        {'adscripcion': 'UMF 095 PONCITLAN'},
                        {'adscripcion': 'UMF 100 JAMAY'},
                        {'adscripcion': 'UMF 165 DEGOLLADO'},
                        {'adscripcion': 'UMF 169 OCOTLAN'},
                        {'adscripcion': 'HGZ 042 PUERTO VALLARTA'},
                        {'adscripcion': 'SUBDELEGACION PUERTO VALLARTA'},
                        {'adscripcion': 'UMF 043 TOMATLAN'},
                        {'adscripcion': 'UMF 170 PUERTO VALLARTA'},
                        {'adscripcion': 'UMF 179 PUERTO VALLARTA'},
                        {'adscripcion': 'HGZ 026 TALA'},
                        {'adscripcion': 'OFNA AUX 139 GUACHINANGO'},
                        {'adscripcion': 'OFNA AUX 142 MIXTLAN'},
                        {'adscripcion': 'OFNA AUX 143 SAN MARCOS'},
                        {'adscripcion': 'OFNA AUX TALA'},
                        {'adscripcion': 'PUESTO ENFERMERIA 144 SAN SEBASTIAN DEL OESTE'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA HOSTOTIPAQUILLO'},
                        {'adscripcion': 'UMF 010 TEQUILA'},
                        {'adscripcion': 'UMF 011 AMATITAN'},
                        {'adscripcion': 'UMF 012 ARENAL'},
                        {'adscripcion': 'UMF 024 AMECA'},
                        {'adscripcion': 'UMF 031 AHUALULCO DEL MERCADO'},
                        {'adscripcion': 'UMF 038 BUENAVISTA'},
                        {'adscripcion': 'UMF 069 ETZATLAN'},
                        {'adscripcion': 'UMF 074 TALPA DE ALLENDE'},
                        {'adscripcion': 'UMF 096 MASCOTA'},
                        {'adscripcion': 'UMF 097 MAGDALENA'},
                        {'adscripcion': 'UMF 098 TEUCHITLAN'},
                        {'adscripcion': 'UMF 137 SAN JUANITO ESCOBEDO'},
                        {'adscripcion': 'HGZ 021 TEPATITLAN DE MORELOS'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 132 SAN JUAN'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 134 VALLE DE GUADALUPE'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 136 CAÑADAS DE OBREGON'},
                        {'adscripcion': 'SUBDELEGACION TEPATITLAN DE MORELOS'},
                        {'adscripcion': 'UMF 044 ARANDAS'},
                        {'adscripcion': 'UMF 085 JALOSTOTITLAN'},
                        {'adscripcion': 'UMF 094 YAHUALICA'},
                        {'adscripcion': 'UMF 128 ACATIC'},
                        {'adscripcion': 'UMF 159 JESUS MARIA'},
                        {'adscripcion': 'UMF 160 CAPILLA DE GUADALUPE'},
                        {'adscripcion': 'UMF 168 TEPATITLAN DE MORELOS'},
                        {'adscripcion': 'UMF 183 SAN IGNACIO CERRO GORDO'},
                        {'adscripcion': 'HGsZ 027 VILLA CORONA'},
                        {'adscripcion': 'OFNA AUX 147 ATEMAJAC DE BRIZUELA'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 152 JUCHITLAN'},
                        {'adscripcion': 'PUESTO DE ENFERMERIA 154 TENAMAXTLAN'},
                        {'adscripcion': 'UMF 025 LA SAUCEDA'},
                        {'adscripcion': 'UMF 029 ESTIPAC'},
                        {'adscripcion': 'UMF 030 BELLAVISTA'},
                        {'adscripcion': 'UMF 056 ACATLAN DE JUAREZ'},
                        {'adscripcion': 'UMF 072 COCULA'},
                        {'adscripcion': 'UMF 073 SAN MARTIN HIDALGO'},
                        {'adscripcion': 'UMF 075 TECOLOTLAN'},
                        {'adscripcion': 'UMF 077 ZACOALCO DE TORRES'},
        ],
        title='Registro de Cédulas Afiliación'

    )




if __name__ == '__main__':
    app.run()
