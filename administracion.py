from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from modelo import *
from datetime import datetime

#
def notificar():
    consulta = '''
        INSERT INTO notificaciones  (rut , fecha , estado , Mensaje) 
        VALUES  ( ? , ? ,'no visto', ? )      
    '''
    estado = "OK"
    try:
        list = request.json
        for dict in list:
            cursor.execute(
                consulta, (dict['rut'], dict['fecha'], dict['Mensaje']))
        conn.commit()
    except Exception as e:
        print("Ocurrió un error", e)
        estado = "Error"
    return jsonify({"status": estado})
notificar.methods=['POST']


#
def contactoEstrecho():
    rut = request.json['rut']
    ini = request.json['inicio']
    fin = request.json['fin']
    try:
        consulta = '''
            SELECT A.rut, count(*) AS contactos
            FROM asistencia AS A,
            (	
            SELECT * 
            FROM asistencia 
            WHERE fecha <=  ? 	AND 
            fecha  >=  ?  		AND  
            rut = ? 
            ) AS LC
            WHERE LC.ID_bloque = A.ID_bloque	AND
                A.rut != LC.rut				    AND
                A.fecha = LC.fecha			    AND
                A.tipo_asistencia  = 1	        AND
                LC.tipo_asistencia = 1		
            GROUP BY A.rut
            ORDER BY A.rut
            '''
        data = cursor.execute(consulta, (fin,ini,rut))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
    except Exception as e:
        print("Ocurrió un error", e)
    return jsonify(results)
contactoEstrecho.methods=['POST']
