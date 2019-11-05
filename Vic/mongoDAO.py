# -*- coding: utf-8 -*-


from pymongo import MongoClient


servidor = 'localhost'
puerto = '27017'


def getMongoClass():
    mongoclient = MongoClient(host=servidor, port=puerto)
    db = mongoclient.giw
    return db.usuarios


def createSingleMongo(filtro):
    clase = getMongoClass()
    res = clase.insert_one(filtro)
    return res


def createMultipleMongo(filtro):
    clase = getMongoClass()
    res = clase.insert_many(filtro)
    return res


def readMongo(filtro, proyectar=None, limite=None, orden=None):
    clase = getMongoClass()

    if proyectar == None and limite == None and orden == None:
        res = clase.find(filtro)

    elif proyectar != None and limite == None and orden == None:
        res = clase.find(filtro, proyectar)

    elif proyectar == None and limite != None and orden == None:
        res = clase.find(filtro).limit(limite)

    elif proyectar == None and limite == None and orden != None:
        res = clase.find(filtro).order(orden)

    elif proyectar != None and limite != None and orden == None:
        res = clase.find(filtro, proyectar).limit(limite)

    elif proyectar != None and limite == None and orden != None:
        res = clase.find(filtro, proyectar).order(orden)

    elif proyectar == None and limite != None and orden != None:
        res = clase.find(filtro).limit(limite).order(orden)

    else:
        res = clase.find(filtro, proyectar).limit(limite).order(orden)
    return res


def updateSingleMongo(filtro, datos):
    clase = getMongoClass()
    res = clase.update_one(filtro, datos)
    return res


def updateMultipleMongo(filtro, datos):
    clase = getMongoClass()
    res = clase.update_many(filtro, datos)
    return res


def deleteSingleMongo(filtro):
    clase = getMongoClass()
    res = clase.delete_one(filtro)
    return res


def deleteMultipleMongo(filtro):
    clase = getMongoClass()
    res = clase.delete_many(filtro)
    return res
