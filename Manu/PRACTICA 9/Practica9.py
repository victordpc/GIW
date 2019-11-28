# -*- coding: utf-8 -*-

##
# LEILA RUIZ CASANOVA
# VÍCTOR DEL PINO CASTILLA
# MANUEL GUERRERO MOÑÚS
# JUAN ANTONIO ÁVILA CATALÁN
#
# declaramos que esta solución es fruto exclusivamente
# de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
# obtenido la soluci´on de fuentes externas, y tampoco hemos compartido nuestra solución
# con nadie. Declaramos adem´as que no hemos realizado de manera deshonesta ninguna otra
# actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
##
import re

from pymongo import MongoClient

from bottle import run, get, request, template, static_file

mongoClient = MongoClient()
db = mongoClient['giw']


def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def is_float(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def show_error_page(msg):
    return template('error_page', error_msg=msg)


@get('/top_countries')
# http://localhost:8080/top_countries?n=3
def top_countries():
    n = request.query.n

    if n is "":
        return show_error_page("Debe introducir el parámetro 'n'")

    if not is_int(n):
        return show_error_page("El parámetro 'n' debe ser número entero")

    n = int(n)

    if n <= 0:
        return show_error_page("El parámetro 'n' debe ser mayor de 0")

    collection = db['usuarios']

    result = collection.aggregate([
        {"$group": {"_id": "$pais", "usuarios": {"$sum": 1}}},
        {"$project": {"_id": 0, "pais": "$_id", "usuarios": "$usuarios"}},
        {"$sort": {"usuarios": -1, "_id": 1}},
        {"$limit": n}
    ])

    result_list = list(result)

    return template('top_countries', results=result_list, page_title="Top countries")


@get('/products')
# http://localhost:8080/products?min=2.34
def products():
    min_price = request.query.min

    if min_price is "":
        return show_error_page("Debe introducir el parámetro 'min'")

    if not is_float(min_price):
        return show_error_page("El parámetro 'min' debe ser un número")

    min_price = float(min_price)

    if min_price < 0:
        return show_error_page("El parámetro 'min' debe ser mayor o igual a 0")

    collection = db['pedidos']

    result = collection.aggregate([
        {"$unwind": "$lineas"},
        {"$match": {"lineas.precio": {"$gte": min_price}}},
        {"$group": {"_id": {"nombre": "$lineas.nombre", "precio": "$lineas.precio"}, "unidades": {"$sum": 1}}},
        {"$project": {"_id": 0, "nombre": "$_id.nombre", "unidades": "$unidades", "precio": "$_id.precio"}}
    ])

    result_list = list(result)

    return template('products', results=result_list, page_title="Products")


@get('/age_range')
# http://localhost:8080/age_range?min=80
def age_range():
    min_users = request.query.min

    if min_users is "":
        return show_error_page("Debe introducir el parámetro 'min'")

    if not is_int(min_users):
        return show_error_page("El parámetro 'min' debe ser un número entero")

    min_users = int(min_users)

    if min_users < 0:
        return show_error_page("El parámetro 'min' debe ser mayor o igual a 0")

    collection = db['usuarios']

    result = collection.aggregate([
        {"$group": {"_id": "$pais", "mp": {"$min": "$edad"}, "mm": {"$max": "$edad"}, "usuarios": {"$sum": 1}}},
        {"$match": {"usuarios": {"$gt": min_users}}},
        {"$project": {"_id": 0, "pais": "$_id", "rango": {"$subtract": ["$mm", "$mp"]}}},
        {"$sort": {"rango": -1, "pais": 1}}
    ])

    result_list = list(result)

    return template('age_range', results=result_list, page_title="Age range")


@get('/avg_lines')
# http://localhost:8080/avg_lines
def avg_lines():
    collection = db['usuarios']

    result = collection.aggregate([
        {"$lookup": {"from": "pedidos", "localField": "_id", "foreignField": "cliente", "as": "pedidosUsuario"}},
        {"$unwind": "$pedidosUsuario"},
        {"$project": {"_id": 1, "pais": 1, "totalLineasPedido": {"$size": "$pedidosUsuario.lineas"}}},
        {"$group": {"_id": "$pais", "totalPedidos": {"$sum": 1}, "totalLineas": {"$sum": "$totalLineasPedido"}}},
        {"$project": {"_id": 0, "pais": "$_id", "numeroMedioDeLineas": {"$divide": ["$totalLineas", "$totalPedidos"]}}}
    ])

    result_list = list(result)

    return template('avg_lines', results=result_list, page_title="Avg lines")


@get('/total_country')
# http://localhost:8080/total_country?c=Alemania
def total_country():
    c = request.query.c

    if c is "":
        return show_error_page("Debe introducir el parámetro 'c'")

    collection = db['usuarios']

    result = collection.aggregate([
        {"$match": {"pais": re.compile(c, re.IGNORECASE)}},
        {"$lookup": {"from": "pedidos", "localField": "_id", "foreignField": "cliente", "as": "pedidosUsuario"}},
        {"$unwind": "$pedidosUsuario"},
        {"$project": {"_id": 0, "pais": 1, "total": "$pedidosUsuario.total"}},
        {"$group": {"_id": "$pais", "totalPedidos": {"$sum": "$total"}}},
        {"$project": {"_id": 0, "pais": "$_id", "totalPedidos": "$totalPedidos"}}
    ])

    result_list = list(result)

    return template('total_country', results=result_list, page_title="Total country")


@get("/css/<filepath:re:.*\\.css>")
def css(filepath):
    return static_file(filepath, root="public/css")


if __name__ == "__main__":
    # No cambiar host ni port ni debug
    run(host='localhost', port=8080, debug=True)
