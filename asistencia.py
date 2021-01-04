from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
from modelo import *
import json


# Recibir el horario del profesor
def horarioProfesor():
    try:
        rut=request.json['rut']
        consulta = '''
            SELECT ID_Bloque,Nombre,Horario_Inicio,ID_sala
	        FROM horario_clase AS HC, clase AS C
	        WHERE C.ID_clase = HC.ID_clase AND
            Rut_Profesor  =  ?
            '''
        data = cursor.execute(consulta, rut)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
    except Exception as e:
        print("Ocurrió un error", e)
    return json.dumps(results, indent=4, default=str)
horarioProfesor.methods=['POST']


#Consultar todos los estudiantes de un horario
def alumnosClase():
    try:
        ID_bloque=request.json['id']
        consulta = '''
            SELECT nombre, ApellidoP, HP.rut
            FROM persona AS P, horario_persona AS HP, horario_clase AS HC
            WHERE P.rut = HP.rut            AND 
            HC.ID_bloque = HP.ID_bloque     AND
	        HC.ID_bloque  =  ?
            '''
        data = cursor.execute(consulta, ID_bloque)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
    except Exception as e:
        print("Ocurrió un error", e)
    return jsonify(results)
alumnosClase.methods=['POST']


#Recibe una lista con los alumnos que asistieron.
def registrarAsistencia():
    consulta = '''
        INSERT INTO asistencia (rut, ID_Bloque, fecha, tipo_asistencia) 
        VALUES (  ?  ,  ?  ,  ?  ,  ?  )        
    '''
    estado = "OK"
    try:
        list = request.json
        for dict in list:
            cursor.execute(
                consulta, (dict['rut'], dict['ID_Bloque'], dict['fecha'], dict['tipo_asistencia']))
        conn.commit()
    except Exception as e:
        print("Ocurrió un error", e)
        estado = "Error"
    return jsonify({"status": estado})
registrarAsistencia.methods=['POST']


#  Consultar todos los estudiantes de un horario
#
def verAsistencias():
    fecha = request.json['fecha']
    ID = request.json['id']
    try:
        consulta = '''
            SELECT  Nombre, ApellidoP, P.rut  
            FROM  asistencia AS A,Persona AS P  
            WHERE  fecha = ? AND ID_Bloque  =  ? AND
            P.rut = A.rut
            '''
        data = cursor.execute(consulta, (fecha, ID))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
    except Exception as e:
        print("Ocurrió un error", e)
    return jsonify(results)
verAsistencias.methods=['POST']