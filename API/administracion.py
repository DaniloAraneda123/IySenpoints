from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from modelo import conectar
from datetime import date
from datetime import timedelta

#


def notificar():
    consulta = '''
        INSERT INTO notificaciones  (rut , fecha , estado , Mensaje) 
        VALUES  ( ? , ? ,'no visto', ? )      
    '''
    estado = "OK"
    try:
        conn,cursor=conectar()
        list = request.json
        for dict in list:
            cursor.execute(
                consulta, (dict['rut'], dict['fecha'], dict['Mensaje']))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Ocurrió un error", e)
        estado = "Error"
    return jsonify({"status": estado})


notificar.methods = ['POST']


#
def contactoEstrecho():
    rut = request.json['rut']
    fin = date.today()
    ini = fin - timedelta(days=15)
    try:
        conn,cursor=conectar()
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
                A.tipo_asistencia  = 'PRESENCIAL'	       AND
                LC.tipo_asistencia = 'PRESENCIAL'		
            GROUP BY A.rut
            ORDER BY A.rut
            '''
        data = cursor.execute(consulta, (fin, ini, rut))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
    except Exception as e:
        print("Ocurrió un error", e)
    return jsonify(results)
contactoEstrecho.methods = ['POST']


# Recibir todas las notificaciones de un usuario ordenado
def getNotificaciones():
    consulta = '''
        SELECT Fecha,Estado,Mensaje FROM
        notificaciones 
        WHERE rut = ? ORDER BY Fecha Desc  
    '''
    results = []
    try:
        conn,cursor=conectar()
        rut = request.json['rut']
        data = cursor.execute(consulta, rut)
        columns = [column[0] for column in cursor.description]
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
    except Exception as e:
        print("Ocurrió un error", e)
        results.append({"status":"error"})
    return jsonify(results)

getNotificaciones.methods = ['POST']


def contactoEstrechoP():
    rut = request.json['rut']
    der = request.json['fin']
    izq = request.json['ini']
    try:
        conn,cursor=conectar()
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
                A.tipo_asistencia  = 'PRECENCIAL'	       AND
                LC.tipo_asistencia = 'PRECENCIAL'		
            GROUP BY A.rut
            ORDER BY A.rut
            '''
        data = cursor.execute(consulta, (der, izq, rut))
        columns = [column[0] for column in cursor.description]
        results = []
        for row in data.fetchall():
            results.append(dict(zip(columns, row)))
        conn.close()
    except Exception as e:
        print("Ocurrió un error", e)
    return jsonify(results)
contactoEstrechoP.methods = ['POST']