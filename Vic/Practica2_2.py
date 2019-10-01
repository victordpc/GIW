import csv
import json
import math

def leer_estaciones():
    resultado = dict()

    with open('Estaciones.csv', encoding="utf8", errors='ignore') as csvestaciones:
        entrada = csv.reader(csvestaciones, delimiter=";")

        for linea in entrada:
            if entrada.line_num == 1:
                continue
            resultado[int(linea[1])] = linea[2]

    return resultado

def leer_museos():
    leer = json.loads(open('Museos.json',encoding="utf8").read())
    return leer['@graph']

def haversine(lat1, lon1, lat2, lon2):
    rad=math.pi/180
    dlat=lat2-lat1
    dlon=lon2-lon1
    R=6372.795477598
    a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia=2*R*math.asin(math.sqrt(a))
    return distancia

def presentar_datos(estaciones,museos):
    return True


estaciones = leer_estaciones()
museos=leer_museos()
presentar_datos(estaciones,museos)