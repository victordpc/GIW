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

import base64
import re
import secrets

import bcrypt as bcrypt
import onetimepass as otp
from bottle import run, post, request, template
from pymongo import MongoClient

##############
# APARTADO 1 #
##############

# 
# Explicación detallada del mecanismo escogido para el almacenamiento de
# contraseñas, explicando razonadamente por qué es seguro
#
# Las contraseñas no son almacenadas en la base de datos, en su lugar, se almacena
# el hash de la misma, de forma que en caso de un acceso no autorizado a la base de datos
# no sería posible suplantar la identidad de los usuarios puesto que no es posible obtener la contraseña
# a partir de su hash (si la función es segura).
#
# Para el proceso de hashing, hemos utilizado la librería 'bcrypt', presente en muchos otros lenguajes
# como PHP. BCrypt está basado en Blowfish (un tipo de cifrado) y es utilizado por defecto en algunas
# distribuciones de Linux. Para la generación del hash utiliza un 'salt' que es prefijado al hash de la contraseña,
# para ser guardado en la base de datos. Con este 'salt' aumentamos con mayor garantía
# que dos contraseñas iguales, generen hashes iguales, dificultando los ataques con diccionarios.
#
# Por defecto, el 'salt' tiene un coste de 2^12 iteraciones (aunque puede configurarse para un valor diferente),
# esto supone un mayor coste de cálculo del hash y por tanto hace más difícil aplicar fuerza bruta. Este valor
# requiere de un balance entre experiencia de usuario, coste de cómputo y seguridad.

client = MongoClient('mongodb://localhost:27017/')
db = client.giw


def find_user_by_nickname(nickname):
    regx = re.compile(nickname, re.IGNORECASE)
    coincidence = db.users.find_one({'nickname': regx})
    return coincidence


def register_new_user(user):
    hashed_pass = bcrypt.hashpw(user['password'].encode('UTF-8'), bcrypt.gensalt())
    user['password'] = hashed_pass
    result = db.users.insert_one(user)
    user['id'] = result.inserted_id
    return user


def password_verify(password, user):
    hashed = user['password']
    return bcrypt.checkpw(password.encode('utf-8'), hashed)


def update_user_password(user, new_pass):
    hashed_pass = bcrypt.hashpw(new_pass.encode('UTF-8'), bcrypt.gensalt())
    user['password'] = hashed_pass
    db.users.update_one({"_id": user['_id']}, {'$set': {'password': hashed_pass}})


@post('/signup')
def signup():
    nickname = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    password = request.forms.get('password')
    password2 = request.forms.get('password2')

    if password != password2:
        return template('error.tpl', {'error': 'Las contraseñas no coinciden'})

    user = find_user_by_nickname(nickname)

    if user is not None:
        return template('error.tpl', {'error': 'El alias de usuario ya existe'})

    register_new_user({'nickname': nickname,
                       'name': name,
                       'country': country,
                       'email': email,
                       "password": password})

    return template('success.tpl', {'msg': 'Bienvenido usuario ' + name})


@post('/change_password')
def change_password():
    nickname = request.forms.get('nickname')
    old_password = request.forms.get('old_password')
    new_password = request.forms.get('new_password')

    user = find_user_by_nickname(nickname)

    if user is not None and password_verify(old_password, user):
        update_user_password(user, new_password)
        return template('success.tpl', {'msg': 'La contraseña del usuario ' + nickname + ' ha sido modificada'})

    return template('error.tpl', {'error': 'Usuario o contraseña incorrectos'})


@post('/login')
def login():
    nickname = request.forms.get('nickname')
    password = request.forms.get('password')

    user = find_user_by_nickname(nickname)

    if user is not None and password_verify(password, user):
        return template('success.tpl', {'msg': 'Bienvenido ' + user['name']})

    return template('error.tpl', {'error': 'Usuario o contraseña incorrectos'})


##############
# APARTADO 2 #
##############

# 
# Explicación detallada de cómo se genera la semilla aleatoria, cómo se construye la URL de registro en Google
# Authenticator y cómo se genera el código QR
#
# --- Semilla aleatoria ---
# A partir de Python 3.6, se incluye la librería 'secrets', la cual permite generar semillas criptográficamente seguras.
# Al ser criptográficamente seguras, se garantiza que dos procesos diferentes no puedan obtener
# semillas iguales (aunque se intenten generarlas simultáneamente)
#
# Hemos utilizado esta librería para generar la clave secreta asociada a cada usuario. El número de bytes utilizados
# lo determina internamente 'secrets', utilizando una cantidad que va aumentando en el tiempo (según se considere
# necesario) https://docs.python.org/3/library/secrets.html (How many bytes should tokens use?)
#
# --- URI de Google Auth ---
# La URI de GAuth se construye siguiendo la especificación enlazada en
# https://github.com/google/google-authenticator/wiki/Key-Uri-Format,
#
# Secreto: Debe estar codificado en Base32. En nuestro caso, primero generamos un token pseudoaleatorio
# criptográficamente seguro a través de la librería 'secrets' y a continuación lo codificamos en Base32 a través de
# la librería 'base64'.
#
# Issuer: No es obligatorio pero sí recomendado, en nuestro caso es GIW_01, sirve para identificar el servicio
# al que está asociado la cuenta.
#
# Label: No es obligatorio pero sí recomendado, Es un par X:Y en el que X es el emisor (servicio) y la Y es la cuenta
# a la que se refiere. Esta etiqueta es recomendable usarla para evitar que hayan colisiones (en un mismo
# dispositivo) entre distintas cuentas del mismo servicio.
#
# Type: Obligatorio, debe ser TOTP o HOTP, en nuestro caso, totp.
#
# --- Código QR ---
# Se utiza la API proporcionada en el enunciado.
#
# Desde el frontend, se hace una petición a la API con la URI de Google Auth en el campo 'data', de forma que se
# genera el QR al cargar la página con la URI proporcionada desde el servidor

def generate_gauth_uri(user):
    nickname = user['nickname']
    secret = user['secret']
    return 'otpauth://totp/GIW_01:' + nickname + '?secret=' + secret + '&issuer=GIW_01'


def totp_verify(token, user):
    secret = user['secret']
    return otp.valid_totp(token, secret)


def generate_random_secret():
    secret = base64.b32encode(secrets.token_bytes())
    return str(secret,'utf-8')


@post('/signup_totp')
def signup_totp():
    nickname = request.forms.get('nickname')
    name = request.forms.get('name')
    country = request.forms.get('country')
    email = request.forms.get('email')
    password = request.forms.get('password')
    password2 = request.forms.get('password2')

    if password != password2:
        return template('error.tpl', {'error': 'Las contraseñas no coinciden'})

    user = find_user_by_nickname(nickname)

    if user is not None:
        return template('error.tpl', {'error': 'El alias de usuario ya existe'})

    secret = generate_random_secret()

    user = register_new_user({'nickname': nickname,
                              'name': name,
                              'country': country,
                              'email': email,
                              'secret': secret,
                              "password": password})

    auth_uri = generate_gauth_uri(user)

    return template('totp_signup_success.tpl',
                    {'nickname': nickname, 'totp_secret': secret, 'google_auth_uri': auth_uri})


@post('/login_totp')
def login_totp():
    nickname = request.forms.get('nickname')
    password = request.forms.get('password')
    totp = request.forms.get('totp')

    user = find_user_by_nickname(nickname)

    if user is not None and password_verify(password, user) and totp_verify(totp, user):
        return template('success.tpl', {'msg': 'Bienvenido ' + user['name']})

    return template('error.tpl', {'error': 'Usuario o contraseña incorrectos'})


if __name__ == "__main__":
    # NO MODIFICAR LOS PARÁMETROS DE run()
    run(host='localhost', port=8080, debug=True)
