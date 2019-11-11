# -*- coding: utf-8 -*-

##
# INCLUIR LA CABECERA AQUI
##

# Incluir los 'import' necesarios
import re
from datetime import datetime

import pymongo
from bottle import request, get, run, template
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.giw


def control_parameters(request, valores):

    datos = request.query.dict
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('error_parameters.tpl', msg=errores)
    return datos


@get('/find_users')
def find_users():

    control_parameters(request, ['name', 'surname', 'birthdate'])
    filters = {}
    if request.query.name:
        filters['name'] = {'$eq': request.query.name}
    if request.query.birthdate:
        filters['birthdate'] = {'$eq': request.query.birthdate}
    if request.query.surname:
        filters['surname'] = {'$eq': request.query.surname}

    coincidences = list(db.usuarios.find(filters))
    return template('all_fields_table.tpl', {'coincidences': coincidences, 'title': 'Resultados de búsqueda'})


@get('/find_email_birthdate')
def email_birthdate():  # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31

    control_parameters(request, ['from', 'to'])
    fromDate = request.query['from']
    toDate = request.query.to

    formattedFromDate = datetime.strptime(fromDate, '%Y-%m-%d')
    formattedToDate = datetime.strptime(toDate, '%Y-%m-%d')

    filters = [{"$addFields": {"convDate": {"$toDate": "$birthdate"}}},
               {"$match": {"convDate": {"$gte": formattedFromDate, "$lte": formattedToDate}}}]

    coincidences = list(db.usuarios.aggregate(filters))
    return template('id_mail_birthdate_table.tpl', {'coincidences': coincidences, 'title': 'Resultados de búsqueda'})


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():  # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc

    control_parameters(request, ['country', 'likes', 'limit', 'ord'])
    country = request.query.country
    likes = request.query.likes.split(',')
    limit = request.query.limit
    ord = request.query.ord

    if ord == 'asc':
        order = 1
    else:
        order = -1

    filters = [{"$addFields": {"convDate": {"$toDate": "$birthdate"}}},
               {"$match": {"address.country": country, "likes": {"$in": likes}}},
               {"$sort": {"convDate": order}},
               {"$limit": int(limit)}]

    coincidences = list(db.usuarios.aggregate(filters))
    return template('all_fields_table.tpl', {'coincidences': coincidences, 'title': 'Resultados de búsqueda'})


@get('/find_birth_month')
def find_birth_month():  # http://localhost:8080/find_birth_month?month=abril

    control_parameters(request, ['month'])
    month = request.query.month

    monthsMap = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    filters = [{"$addFields": {"convDate": {"$toDate": "$birthdate"}}},
               {"$addFields": {"month": {"$month": '$convDate'}}},
               {"$match": {"month": monthsMap[month]}},
               {"$sort": {"convDate": 1}}]

    coincidences = list(db.usuarios.aggregate(filters))
    return template('all_fields_table.tpl', {'coincidences': coincidences, 'title': 'Resultados de búsqueda'})


@get('/find_likes_not_ending')
def find_likes_not_ending():  # http://localhost:8080/find_likes_not_ending?ending=s

    control_parameters(request, ['ending'])
    ending = request.query.ending

    regx = re.compile(ending + "$", re.IGNORECASE)
    filters = {"likes": {"$not": regx}}

    coincidences = list(db.usuarios.find(filters))
    return template('all_fields_table.tpl', {'coincidences': coincidences, 'title': 'Resultados de búsqueda'})


@get('/find_leap_year')
def find_leap_year():  # http://localhost:8080/find_leap_year?exp=20

    control_parameters(request, ['exp'])
    exp = request.query.exp

    filters = [{"$addFields": {"convDate": {"$toDate": "$birthdate"}}},
               {"$addFields": {"year": {"$year": '$convDate'}}},
               {"$match": {"$or": [{"$and": [{"year": {"$mod": [4, 0]}}, {"year": {"$not": {"$mod": [100, 0]}}}]},
                                   {"year": {"$mod": [400, 0]}}],
                           "credit_card.expire.year": exp
                           }
                }
               ]

    coincidences = list(db.usuarios.aggregate(filters))
    return template('all_fields_table.tpl', {'coincidences': coincidences, 'title': 'Resultados de búsqueda'})


###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
