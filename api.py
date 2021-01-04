from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from modelo import *
from datetime import datetime
import json,perfilUsuario,asistencia,administracion

app = Flask(__name__)
CORS(app)


#Retorna un formulario con los datos el alumnos 
# (POST: rut)
app.add_url_rule('/getPerfil',view_func=perfilUsuario.verPerfil)


#Retorna el horario de un alumno 
# (POST: rut)
app.add_url_rule('/getHorario',view_func=perfilUsuario.verHorario)


#Retorna el horario del profesor 
# (POTS: rut)
app.add_url_rule('/horarioProfesor',view_func=asistencia.horarioProfesor)


#Retorna una lista con todos los alumnos inscritos en un bloque 
# (POST: id)
app.add_url_rule('/alumnosClase',view_func=asistencia.alumnosClase)


#Recibe una lista con los alumnos que asistieron
#(POST: list[rut,ID_Bloque,fecha,tipo_asistencia])
app.add_url_rule('/registrarAsistencia',view_func=asistencia.registrarAsistencia)


#Retorna una lista con todos los alumnos que asistieron
#(POST: fecha,id)
app.add_url_rule('/verAsistencias',view_func=asistencia.verAsistencias)


#Recibe una lista de alumnos a los que se le notificara
#(POST: rut,fecha,mensaje )
app.add_url_rule('/notificar',view_func=administracion.notificar)


#Retorna una lista con los estudiantes que tubieron un contacto estrecho
#(POST: inicio,fin,rut)
app.add_url_rule('/contactosEstrechos',view_func=administracion.contactoEstrecho)


if __name__ == '__main__':
    app.run(host='192.168.0.103',debug=True, port=5000)
    
