from bottle import request, run, route, get, template
import re
from pymongo import ASCENDING, DESCENDING, MongoClient, CursorType


cliente=MongoClient()
c = cliente.giw.usuarios

@get('/find_users')
def find_users():
    # http://localhost:8080/find_users?name=Luz
    # http://localhost:8080/find_users?name=Luz&surname=Romero
    # http://localhost:8080/find_users?name=Luz&surname=Romero&birthdate=2006-08-14
    
    filtro={}

    if request.query.name != '':
        urlname= request.query.name
        filtro['name']=urlname
    if request.query.surname != '':
        urlsurname=request.query.surname
        filtro['surname']=urlsurname
    if request.query.birthdate != '':
        urlbth = request.query.birthdate
        filtro['birthdate']=urlbth
    

    resultado=list(c.find(filtro))
    print(resultado)





@get('/find_email_birthdate')
def email_birthdate():
    # http://localhost:8080/find_email_birthdate?from=1973-01-01&to=1990-12-31
    datos = request.query.dict
    valores = ['from', 'to']
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('plantillas/errorParametros.tpl', msg=errores)
    elif len(datos) != 2:
        return template('plantillas/errorNumParametros.tpl', numero=2, actual=len(datos), msg=datos.keys())

    busqueda = dict()

    busqueda['$gte'] = datos['from'][0]
    busqueda['$lte'] = datos['to'][0]
    proyectar = {'_id': 1, 'email': 1, 'birthdate': 1}

    resultado = list(mDao.readMongo({'birthdate': busqueda}, proyectar))
    return resultado


@get('/find_country_likes_limit_sorted')
def find_country_likes_limit_sorted():
    # http://localhost:8080/find_country_likes_limit_sorted?country=Irlanda&likes=movies,animals&limit=4&ord=asc
    datos = request.query.dict
    valores = ['country', 'likes', 'limit', 'ord']
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('plantillas/errorParametros.tpl', msg=errores)
    elif len(datos) != 4:
        return template('plantillas/errorNumParametros.tpl', numero=4, actual=len(datos), msg=datos.keys())

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
    datos = request.query.dict
    valores = ['month']
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('plantillas/errorParametros.tpl', msg=errores)
    elif len(datos) != 1:
        return template('plantillas/errorNumParametros.tpl', numero=1, actual=len(datos), msg=datos.keys())

    busqueda = {
        "$where": "this.birthdate.split('-')[1] == " + str(meses[datos['month'][0]])}
    orden = [('birthdate', ASCENDING)]

    resultado = list(mDao.readMongo(busqueda, None, None, orden))

    return resultado


@get('/find_likes_not_ending')
def find_likes_not_ending():
    # http://localhost:8080/find_likes_not_ending?ending=s
    datos = request.query.dict
    valores = ['ending']
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('plantillas/errorParametros.tpl', msg=errores)
    elif len(datos) != 1:
        return template('plantillas/errorNumParametros.tpl', numero=1, actual=len(datos), msg=datos.keys())

    expresion = re.compile(re.escape(datos['ending'][0])+'$',re.IGNORECASE)
    busqueda = {'likes':expresion }

    resultado = list(mDao.readMongo(busqueda))
    return resultado


@get('/find_leap_year')
def find_leap_year():
    # http://localhost:8080/find_leap_year?exp=20
    datos = request.query.dict
    valores = ['ending'] 
    errores = list(filter(lambda x: x not in valores, datos.keys()))

    if len(errores) > 0:
        return template('plantillas/errorParametros.tpl', msg=errores)
    elif len(datos) != 1:
        return template('plantillas/errorNumParametros.tpl', numero=1, actual=len(datos), msg=datos.keys())

    busqueda = {'likes': {'$all': re.compile(
        datos['ending'][0], re.IGNORECASE)}}

    resultado = list(mDao.readMongo(busqueda))
    return resultado


###################################
# NO MODIFICAR LA LLAMADA INICIAL #
###################################
if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True)
