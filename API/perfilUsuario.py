from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
from modelo import conectar
import json

#
#
#
def verPerfil():
    dict = {}
    try:
        conn,cursor=conectar()
        rut=request.json['rut']
        consulta = '''
            SELECT * 
            FROM Persona 
            WHERE Rut=?
            '''
        data = cursor.execute(consulta, str(rut))
        columns = [column[0] for column in cursor.description]
        row = data.fetchone()
        if row is not None:
            for i in range(len(columns)):
                dict[columns[i]] = row[i]
        else:
            dict['status'] = 'no existe'
        conn.close()
    except Exception as e:
        print("Ocurrió un error", e)
        dict['status'] = 'error'
    return jsonify(dict)
verPerfil.methods=['POST']

#
#
#
def verHorario():
    try:
        conn,cursor=conectar()
        rut=request.json['rut']
        consulta = '''
            SELECT Nombre,ID_Sala,Horario_Inicio,Dia
            FROM rastreo.dbo.Horario_Persona AS HP,rastreo.dbo.Horario_Clase AS HC, rastreo.dbo.Clase AS C
            WHERE	HC.ID_Bloque=HP.ID_Bloque AND C.ID_Clase = HC.ID_Clase AND
            rut=? AND Anio=2020 AND Semestre = 2
            '''
        data = cursor.execute(consulta, rut)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
    except Exception as e:
        print("Ocurrió un error", e)
        return jsonify({"cod":"error"})
    return json.dumps(results, indent=4, sort_keys=True, default=str)
verHorario.methods=['POST']