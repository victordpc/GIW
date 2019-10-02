import csv

medidas = {1: 'Dióxido de Azufre', 6: 'Monóxido de Carbono', 7: 'Monóxido de Nitrógeno', 8: 'Dióxido de Nitrógeno', 9: 'Partículas < 2.5 µm', 10: 'Partículas < 10 µm', 12: 'Óxidos de Nitrógeno', 14: 'Ozono',
           20: 'Tolueno', 30: 'Benceno', 35: 'Etilbenceno', 37: 'Metaxileno', 38: 'Paraxileno', 39: 'Ortoxileno', 42: 'Hidrocarburos totales (Hexano)', 43: 'Metano', 44: 'Hidrocarburos no metánicos (hexano)'}


def leer_estaciones():
    resultado = dict()

    with open('Estaciones.csv', encoding="utf8", errors='ignore') as csvestaciones:
        entrada = csv.reader(csvestaciones, delimiter=";")

        for linea in entrada:
            if entrada.line_num == 1:
                continue
            resultado[int(linea[1])] = linea[2]

    return resultado


def procesar_datos():
    datos = dict()
    with open('Contaminación.csv', encoding="utf8", errors='ignore') as csvarchivo:
        entrada = csv.reader(csvarchivo, delimiter=";")

        for i in entrada:
            if entrada.line_num == 1:
                continue

            estacion = int(i[2])
            magnitud = int(i[3])

            if estacion not in datos:
                datos[estacion] = dict()

            valor = 0.0
            if magnitud in datos[estacion]:
                valor = datos[estacion][magnitud]

            # Columnas de valores de contaminación [7-68]
            for celda in range(8, 69, 2):
                if i[celda].upper() == "V":
                    valor = valor+float(i[celda-1])

            datos[estacion][magnitud] = valor
    return datos

def presentar_datos(datos):
    # Cabecera
    cabecera='Estación'
    for contaminanteM in medidas.values():
        cabecera=cabecera+'\t'+contaminanteM
    print(cabecera)

    for estacion in datos:
        datosSalida = estaciones[estacion]

        for valor in medidas.keys():
            if valor in datos[estacion]:
                datosSalida=datosSalida+'\t'+str(datos[estacion][valor])
            else:
                datosSalida=datosSalida+'\t'+'---'
        print(datosSalida)


def grabar_fichero(datos):

    with open('Salida.csv', 'w', encoding='utf8') as destino:
        salida = csv.writer(destino,delimiter=';')

        # Cabecera
        cabecera=['Estación']
        for contaminanteM in medidas.values():
            cabecera.append(contaminanteM)
            cabecera.append("Valor")
        salida.writerow(cabecera)

        for estacion in datos:
            datosSalida = [estaciones[estacion]]

            for clave,valor in medidas.items():
                datosSalida.append(valor)
                if clave in datos[estacion]:
                    datosSalida.append(datos[estacion][clave])
                else:
                    datosSalida.append('---')
            salida.writerow(datosSalida)


estaciones = leer_estaciones()
datos = procesar_datos()
presentar_datos(datos)
grabar_fichero(datos)
