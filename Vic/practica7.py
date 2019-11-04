# -*- coding: utf-8 -*-

##
# INCLUIR LA CABECERA AQUI
##

# Incluir los 'import' necesarios
from bottle import request, run, route, get, template
from pymongo import MongoClient


@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14
    datos = request.query
    valores = ['name', 'surname', 'birthdate']
    errores = filter(lambda x: x not in valores, datos.keys())

    if len(errores) > 0:
        return template('\plantillas\errorParametros.tpl', msg=errores)

    busqueda = dict()
    for clave, valor in datos.items():
        busqueda[clave] = valor
    resultado = readMongo(busqueda)


@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    datos = request.query
    valores = ['from', 'to']
    errores = filter(lambda x: x not in valores, datos.keys())

    if len(errores) > 0:
        return template('\plantillas\errorParametros.tpl', msg=errores)

    busqueda = dict()

    busqueda['$gte'] = datos['from']
    busqueda['$lte'] = datos['to']

    resultado = readMongo(['birthdate']=busqueda)
    # users.find({nhijos: {$gte: 2, $lte: 5} })


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    datos = request.query
    valores = ['countr', 'likes', 'limit', 'ord']
    errores = filter(lambda x: x not in valores, datos.keys())

    if len(errores) > 0:
        return template('\plantillas\errorParametros.tpl', msg=errores)

    busqueda = dict()

    busqueda['$gte'] = datos['from']
    busqueda['$lte'] = datos['to']

    resultado = readMongo(['birthdate']=busqueda)
    # users.find({nhijos: {$gte: 2, $lte: 5} })


@get('/find_birth_month')
def find_birth_month():
    # http://localhost:8080/find_birth_month?month=abril


@get('/find_likes_not_ending')
def find_likes_not_ending():
    # http://localhost:8080/find_likes_not_ending?ending=s


@get('/find_leap_year')
def find_leap_year():
    # http://localhost:8080/find_leap_year?exp=20


def createSingleMongo(filtro):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.insert_one(filtro)
    return res


def createMultipleMongo(filtro):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.insert_many(filtro)
    return res


def readMongo(filtro):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.find(filtro)
    return res


def updateSingleMongo(filtro, datos):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.update_one(filtro, datos)
    return res


def updateMultipleMongo(filtro, datos):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.update_many(filtro, datos)
    return res


def deleteSingleMongo(filtro):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.delete_one(filtro)
    return res


def deleteMultipleMongo(filtro):
    mongoclient = MongoClient(host='localhost', port='27017')
    db = mongoclient.giw
    clase = db.usuarios
    res = clase.delete_many(filtro)
    return res


    ###################################
    # NO MODIFICAR LA LLAMADA INICIAL #
    ###################################
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
