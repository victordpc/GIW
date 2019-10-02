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
            if texto == [] or entrada.line_num == 1:
                continue

            tipo = ""
            max = 0.0
            for i in range(2, len(texto), 2):
                if texto[i] != '---' and float(texto[i]) > max:
                    max = float(texto[i])
                    tipo = texto[i-1]
            resultado[texto[0]] = {
                "Nombre": texto[0], "Valor": max, "Tipo": tipo}
    return resultado


def espaciado_tabla(tam_cabecera, texto, lineaPantalla):
    espaciado = (tam_cabecera-len(texto))//8
    if (tam_cabecera-len(texto)) % 8 != 0:
        espaciado = espaciado + 1
    for i in range(espaciado):
        lineaPantalla = lineaPantalla+'\t'
    return lineaPantalla


def presentar_datos(estaciones, valores, museos):
    resultado = dict()
    resultado["año"] = 2019
    resultado["fuente"] = "Ayuntamiento de Madrid"
    listaMuseos = list()

    #                   0                        80           24                 24           24                 24         16
    cabeceraPantalla = 'Museo\t\t\t\t\t\t\t\t\t\tEstacion1\t\tTipoContaminante1\tEstacion2\t\tTipoContaminante2\tEstacion3\t\tTipoContaminante3'
    print(cabeceraPantalla)

    cabeceraPantalla = ''
    for i in range(224):
        cabeceraPantalla = cabeceraPantalla+'-'
    print(cabeceraPantalla)

    for museo in museos:
        if 'location' not in museo:
            continue

        lineaPantalla = museo['title']
        lineaPantalla = espaciado_tabla(80, lineaPantalla, lineaPantalla)

        datos = dict()
        datos["museo"] = museo['title']

        # Calculamos las distancias del museo a todas las estaciones
        distancias = calcular_distancias(estaciones, museo)

        elemento = "Estación 1"
        espacioEstacion = 24
        espacioContaminante = 24

        lineaPantalla = agregar_linea(
            distancias, datos, elemento, valores, lineaPantalla, espacioEstacion, espacioContaminante)

        elemento = "Estación 2"
        espacioEstacion = 24
        espacioContaminante = 24

        lineaPantalla = agregar_linea(
            distancias, datos, elemento, valores, lineaPantalla, espacioEstacion, espacioContaminante)

        elemento = "Estación 3"
        espacioEstacion = 24
        espacioContaminante = 16

        lineaPantalla = agregar_linea(
            distancias, datos, elemento, valores, lineaPantalla, espacioEstacion, espacioContaminante)

        print(lineaPantalla)
        listaMuseos.append(datos)

    resultado["museos"] = listaMuseos

    with open("Salida.json", "w", encoding='utf8') as salida:
        json.dump(resultado, salida, indent=2)


def calcular_distancias(estaciones, museo):
    distancias = list()
    for valor in estaciones.values():
        distancia = haversine(float(valor[2]), float(
            valor[1]), museo['location']['latitude'], museo['location']['longitude'])
        distancias.append([distancia, valor[0]])
    return distancias


def agregar_linea(distancias, datos, elemento, valores, lineaPantalla, espacioEstacion, espacioContaminante):
    estacion = min(item for item in distancias)
    datos[elemento] = dict()
    datos[elemento]["Nombre"] = estacion[1]
    datos[elemento]["Valor"] = valores[estacion[1]]["Valor"]
    datos[elemento]["Tipo"] = valores[estacion[1]]["Tipo"]

    lineaPantalla = lineaPantalla+estacion[1]
    lineaPantalla = espaciado_tabla(
        espacioEstacion, estacion[1], lineaPantalla)

    lineaPantalla = lineaPantalla+valores[estacion[1]]["Tipo"]
    lineaPantalla = espaciado_tabla(
        espacioContaminante, valores[estacion[1]]["Tipo"], lineaPantalla)

    distancias.remove(estacion)
    return lineaPantalla


estaciones = leer_estaciones()
museos = leer_museos()
valores = leer_valores()
presentar_datos(estaciones, valores, museos)
