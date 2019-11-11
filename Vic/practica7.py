# -*- coding: utf-8 -*-

# (Nombres completos de los autores) declaramos que esta solución es fruto exclusivamente
# de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
# obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
# con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
# actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

# Incluir los 'import' necesarios
from bottle import request, run, route, get, template
import mongoDAO as mDao
import re
from pymongo import ASCENDING, DESCENDING

''' Establecemos aqui los parametros iniciales, deberian estar dentro del main, pero como no lo podemos tocar aqui los ponemos
'''
meses = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11,
         'diciembre': 12}


def control_parameters(request, valores):
    datos = request.query.dict
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('plantillas/errorParametros.tpl', msg=errores)
    return datos


@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14
    datos = control_parameters(request, ['name', 'surname', 'birthdate'])

    busqueda = dict()
    for clave, valor in datos.items():
        busqueda[clave] = valor[0]
    recuperado = list(mDao.readMongo(busqueda))

    print(recuperado)

    return template('plantillas/mostrarUsuario.tpl', datos=recuperado)


@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    datos = control_parameters(request, ['from', 'to'])

    busqueda = dict()

    busqueda['$gte'] = datos['from'][0]
    busqueda['$lte'] = datos['to'][0]
    proyectar = {'_id': 1, 'email': 1, 'birthdate': 1}

    resultado = list(mDao.readMongo({'birthdate': busqueda}, proyectar))
    return resultado


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    datos = control_parameters(request, ['country', 'likes', 'limit', 'ord'])
    busqueda = dict()

    busqueda['address.country'] = datos['country'][0]
    busqueda['likes'] = ({'$all': datos['likes'][0].split(',')})

    if datos['ord'][0] == 'asc':
        orden = [('birthdate', ASCENDING)]
    else:
        orden = [('birthdate', DESCENDING)]
    limite = int(datos['limit'][0])

    resultado = list(mDao.readMongo(busqueda, None, limite, orden))
    return resultado
    # users.find({nhijos: {$gte: 2, $lte: 5} })


@get('/find_birth_month')
def find_birth_month():
    # http://localhost:8080/find_birth_month?month=abril
    datos = control_parameters(request, ['month'])

    busqueda = {
        "$where": "this.birthdate.split('-')[1] == " + str(meses[datos['month'][0]])}
    orden = [('birthdate', ASCENDING)]

    resultado = list(mDao.readMongo(busqueda, None, None, orden))

    return resultado


@get('/find_likes_not_ending')
def find_likes_not_ending():
    # http://localhost:8080/find_likes_not_ending?ending=s
    datos = control_parameters(request, ['ending'])

    expresion = re.compile(re.escape(datos['ending'][0])+'$', re.IGNORECASE)
    busqueda = {'likes': expresion}

    resultado = list(mDao.readMongo(busqueda))
    return resultado


@get('/find_leap_year')
def find_leap_year():
    # http://localhost:8080/find_leap_year?exp=20
    datos = control_parameters(request, ['exp'])

    busqueda = {'likes': {'$all': re.compile(
        datos['ending'][0], re.IGNORECASE)}}

    resultado = list(mDao.readMongo(busqueda))
    return resultado


###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
