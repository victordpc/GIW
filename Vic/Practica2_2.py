import csv
import json
import math
import sys


def leer_estaciones():
    resultado = dict()

    with open('Estaciones.csv', encoding="utf8", errors='ignore') as csvestaciones:
        entrada = csv.reader(csvestaciones, delimiter=";")

        for linea in entrada:
            if entrada.line_num == 1:
                continue
            resultado[int(linea[1])] = [linea[2], linea[24], linea[25]]

    return resultado


def leer_museos():
    leer = json.loads(open('Museos.json', encoding="utf8").read())
    return leer['@graph']


def haversine(lat1, lon1, lat2, lon2):
    rad = math.pi/180
    dlat = lat2-lat1
    dlon = lon2-lon1
    R = 6372.795477598
    a = (math.sin(rad*dlat/2))**2 + math.cos(rad*lat1) * \
        math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia = 2*R*math.asin(math.sqrt(a))
    return distancia


def leer_valores():
    resultado = dict()
    with open('Salida.csv', encoding='utf8', errors='ignore') as documento:
        entrada = csv.reader(documento, delimiter=";")

        for texto in entrada:
            if texto == []:
                continue
            if entrada.line_num == 1:
                cabecera = texto
                continue

            tipo = ""
            max = 0.0
            for i in range(1, len(texto)):
                if texto[i] != '---' and float(texto[i]) > max:
                    max = float(texto[i])
                    tipo = cabecera[i]
            resultado[texto[0]] = {
                "Nombre": texto[0], "Valor": max, "Tipo": tipo}
    return resultado


def presentar_datos(estaciones, valores, museos):
    resultado = dict()
    resultado["año"] = 2019
    resultado["fuente"] = "Ayuntamiento de Madrid"
    listaMuseos = list()

    for museo in museos:
        if 'location' not in museo:
            continue

        datos = dict()
        datos["museo"] = museo['title']

        # Calculamos las distancias del museo a todas las estaciones
        distancias = list()
        for valor in estaciones.values():
            distancia = haversine(float(valor[2]), float(
                valor[1]), museo['location']['latitude'], museo['location']['longitude'])
            distancias.append([distancia, valor[0]])

        estacion1 = min(item for item in distancias)

        datos["Estación 1"]=dict()
        datos["Estación 1"]["Nombre"]=estacion1[1]
        datos["Estación 1"]["Valor"]=valores[estacion1[1]]["Valor"]
        datos["Estación 1"]["Tipo"]=valores[estacion1[1]]["Tipo"]

        listaMuseos.append(datos)

    resultado["museos"] = listaMuseos

    with open("Salida.json", "w", encoding='utf8') as salida:
        json.dump(resultado, salida, indent=2)


estaciones = leer_estaciones()
museos = leer_museos()
valores = leer_valores()
presentar_datos(estaciones, valores, museos)


# {
#   "año": 2019,
#   "fuente": "Ayuntamiento de Madrid",
#   "museos": [
#     {
#       "museo": "Museo xxxx",
#       "Estación 1": {
#         "Nombre": "Estación X",
#         "Valor": XX,
#         "Tipo":TipoContaminante
#       },
#       "Estación 2": {
#         "Nombre": "Estación Y",
#         "Valor": XX,
#         "Tipo":TipoContaminante
#       },
#       "Estación 3": {
#         "Nombre": "Estación Z",
#         "Valor": XX,
#         "Tipo":TipoContaminante
#       }
#     },
#     ...
#     {
#       "museo": "Museo xxxx",
#       "Estación 1": {
#         "Nombre": "Estación X",
#         "Valor": XX,
#         "Tipo":TipoContaminante
#       },
#       "Estación 2": {
#         "Nombre": "Estación Y",
#         "Valor": XX,
#         "Tipo":TipoContaminante
#       },
#       "Estación 3": {
#         "Nombre": "Estación Z",
#         "Valor": XX,
#         "Tipo":TipoContaminante
#       }
#     }
#   ]
# }
