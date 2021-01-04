from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
from modelo import *
import json

#
#
#
def verPerfil():
    try:
        rut=request.json['rut']
        print(rut)
        consulta = '''
            SELECT * 
            FROM Persona 
            WHERE Rut=?
            '''
        data = cursor.execute(consulta, rut)
        columns = [column[0] for column in cursor.description]
        row = data.fetchone()
        dict = {}
        if row is not None:
            for i in range(len(columns)):
                dict[columns[i]] = row[i]
            del dict['Rol']
        else:
            dict['status'] = 'no existe'
    except Exception as e:
        print("Ocurrió un error", e)
    return jsonify(dict)
verPerfil.methods=['POST']

#
#
#
def verHorario():
    try:
        rut=request.json['rut']
        consulta = '''
            SELECT Nombre,ID_Sala,Horario_Inicio
            FROM rastreo.dbo.Horario_Persona AS HP,rastreo.dbo.Horario_Clase AS HC, rastreo.dbo.Clase AS C
            WHERE	HC.ID_Bloque=HP.ID_Bloque AND C.ID_Clase = HC.ID_Clase AND
            rut=?
            '''
        data = cursor.execute(consulta, rut)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
    except Exception as e:
        print("Ocurrió un error", e)
    return json.dumps(results, indent=4, sort_keys=True, default=str)
verHorario.methods=['POST']