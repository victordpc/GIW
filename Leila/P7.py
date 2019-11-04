# -*- coding: utf-8 -*-
 
##
#
# GIW
# Práctica 6
# Grupo 1
# Juan Antonio, Manuel, Víctor y Leila.
#
# Juan Antonio Ávila Catalán, Manuel Guerrero Moñús, Víctor del Pino Castilla y Leila Ruiz Casanova
# declaramos que esta solucion es fruto exclusivamente de nuestro trabajo personal. 
# No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solucion de fuentes externas,
#  y tampoco hemos compartido nuestra solucion con nadie. 
# Declaramos ademas que no hemos realizado de manera deshonesta ninguna otra actividad
# que pueda mejorar nuestros resultados ni perjudicar los resultados de los demas.
#  
##

# Incluir los 'import' necesarios

import pymongo
from bottle import get, run
from pymongo import MongoClient



@get('/find_users')
def find_users():
    datos = request.query
    validos = ['name', 'surname', 'birthdate']
    errores = filter(lambda x: x not in validos, datos.keys())

    if len(errores) > 0:
        return template('\plantillas\errorParametros.tpl', msg = errores)

    name = datos.name
    surname = datos.surname
    birthdate = datos.birthdate

    mongoclient = MongoClient()
    db = mongoclient.giw
    c = db.usuarios

    persona = {'name': name, 'surname': surname, 'birthdate': birthdate}
    res = c.find(persona)

    return template('\plantillas\buscarUsuario', msg = res)

    
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14


@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc


@get('/find_birth_month')
def find_birth_month():
    # http://localhost:8080/find_birth_month?month=abril


@get('/find_likes_not_ending')
def find_likes_not_ending():
    # http://localhost:8080/find_likes_not_ending?ending=s


@get('/find_leap_year')     
def find_leap_year():
    # http://localhost:8080/find_leap_year?exp=20




###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host='localhost',port=8080,debug=True)
