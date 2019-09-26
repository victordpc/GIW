import csv

def procesar_datos():
    datos = dict()
    with open('Contaminación.csv',encoding="utf8",errors='ignore') as csvarchivo:
        entrada = csv.reader(csvarchivo, delimiter=";")

        for i in entrada:
            if entrada.line_num==1:
                continue
            
            if i[2] not in datos:
                datos[i[2]]=dict()
            
            valor=0.0
            if i[3] in datos[i[2]]:
                valor = datos[i[2]][i[3]]

            # Columnas de valores de contaminación [7-68]
            for celda in range(8,69,2):
                if i[celda].upper()=="V":
                    valor = valor+float(i[celda-1])

            datos[i[2]][i[3]]=valor
    return datos


def presentar_datos(datos):
    
    with open('Salida.csv','w') as destino:
        for estacion in datos:
            for contaminante,subtotal in datos[estacion]:
                print(estacion,contaminante,subtotal)


datos=procesar_datos()
presentar_datos(datos)

