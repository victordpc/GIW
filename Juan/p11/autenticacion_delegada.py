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

import bottle
import secrets
from bottle import run, get, template, request
from beaker.middleware import SessionMiddleware
import requests

# Resto de importaciones
# Credenciales.
# https://developers.google.com/identity/protocols/OpenIDConnect#appsetup
# Copiar los valores adecuados.

CLIENT_ID = '69411229963-1ts8t835hcmqvfoa9gnio346gmvu1fdn.apps.googleusercontent.com'
CLIENT_SECRET = '4qeHPY6_gdp-3P_oTu5EWVzu'
REDIRECT_URI = "http://localhost:8080/token"

# Fichero de descubrimiento para obtener el 'authorization endpoint' y el
# 'token endpoint'
# https://developers.google.com/identity/protocols/OpenIDConnect#authenticatingtheuser
DISCOVERY_DOC = "https://accounts.google.com/.well-known/openid-configuration"

# Token validation endpoint para decodificar JWT
# https://developers.google.com/identity/protocols/OpenIDConnect#validatinganidtoken
TOKENINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session',
    'session.auto': True,
}

app = SessionMiddleware(bottle.app(), session_opts)


def session_set(key, val):
    bottle.request.environ['beaker.session'][key] = val


def session_get(key):
    print(bottle.request.environ['beaker.session'])
    return bottle.request.environ['beaker.session'][key]


def openid_endpoint_of(key):
    doc = requests.get(url=DISCOVERY_DOC).json()
    return doc[key]


@get('/login_google')
def login_google():
    csrf_token = secrets.token_urlsafe()
    session_set('token', csrf_token)
    auth_endpoint = openid_endpoint_of('authorization_endpoint')
    auth_url = auth_endpoint + "?client_id=" + CLIENT_ID + "&response_type=code&scope=openid%20email&redirect_uri=" + REDIRECT_URI + "&state=" + csrf_token
    return template('login_google.tpl', {"auth_url": auth_url, "client_id": CLIENT_ID, "token": csrf_token})


@get('/token')
def token():
    state = request.query['state']
    csrf_token = session_get('token')
    if state != csrf_token:
        return template('error.tpl', {"error": "El token csrf no es válido, vuelva a iniciar el proceso"})

    token_endpoint = openid_endpoint_of('token_endpoint')
    request_data = {
        "code": request.query['code'],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(url=token_endpoint, data=request_data)
    if not response.ok:
        return template('error.tpl', {"error": "No se ha podido completar el proceso de autenticación"})

    jwt = response.json()['id_token']
    response = requests.get(url=TOKENINFO_ENDPOINT, params={"id_token": jwt})
    if not response.ok:
        return template('error.tpl', {"error": "No se ha podido completar el proceso de autenticación"})

    decoded_jwt = response.json()

    return template('success.tpl', {"email": decoded_jwt['email']})


if __name__ == "__main__":
    # Usar sesiones requiere crear objetos adicionales y modificar los parámetros de run()
    run(app=app, host='localhost', port=8080, debug=True)
