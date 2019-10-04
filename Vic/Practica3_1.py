import urllib.request
from xml.etree import ElementTree


def obtenerDatos():
    x = urllib.request.urlopen(
        'https://datos.madrid.es/egob/catalogo/200761-0-parques-jardines.xml')
    a = x.read()
    a = a.decode("utf-8")

    with open("catalogo.xml", "w", encoding="utf8") as catalogo:
        catalogo.write(str(a))


def procesar_XML():
    datos = dict()
    with open("catalogo.xml", "rt", encoding="utf8") as fichero:
        arbol = ElementTree.parse(fichero)

    for nodo in arbol.iter("contenido"):
        parque = dict()

        for elementos in nodo[1]:
            if elementos.attrib['nombre'] == 'LOCALIZACION':
                for direccion in elementos:
                    if 'NOMBRE-VIA' == direccion.attrib['nombre']:
                        nombre_via = direccion.text
                    elif 'CLASE-VIAL' == direccion.attrib['nombre']:
                        tipo_via = direccion.text+' '
                    elif 'NUM' == direccion.attrib['nombre']:
                        numero = ', ' + direccion.text
                    elif 'LOCALIDAD' == direccion.attrib['nombre']:
                        localidad = '. ' + direccion.text
                    elif 'PROVINCIA' == direccion.attrib['nombre']:
                        provincia = '. ' + direccion.text
                    elif 'CODIGO-POSTAL' == direccion.attrib['nombre']:
                        codigo_postal = ', ' + direccion.text

                cadena = tipo_via + nombre_via + numero + localidad + provincia + codigo_postal

                if cadena != "":
                    parque[elementos.attrib['nombre']] = cadena

            else:
                parque[elementos.attrib['nombre']] = elementos.text

        datos[parque['NOMBRE']] = parque
    return datos


def pedir_entrada(datos):
    mostrar_listado(datos.keys())
    entrada = input()
    continuar = True
    while continuar:
        if entrada in datos.keys():
            mostrar_informacion(datos[entrada])

            mostrar_listado(datos.keys())
            entrada = input()

        elif entrada.upper() == 'FIN':
            continuar = False
        else:
            mostrar_listado(datos.keys())
            print('\n\nEl parque', entrada,
                  'no ha sido encontrado, vuelva a introduir un nombre')
            entrada = input()



def mostrar_listado(datos):
    for elemento in datos:
        print(elemento)
    print('\nPara salir del programa introduzca FIN')


def mostrar_informacion(parque):
    print('\n\n')
    if 'NOMBRE' in parque:
        print('Nombre del parque:\n')
        print(parque['NOMBRE']+'\n')

    if 'DESCRIPCION-ENTIDAD' in parque:
        print('Descripción del parque:\n')
        print(parque['DESCRIPCION-ENTIDAD']+'\n')

    if 'DESCRIPCION' in parque:
        print('Información conservación:\n')
        print(parque['DESCRIPCION']+'\n')

    if 'HORARIO' in parque:
        print('Horario:\n')
        print(parque['HORARIO']+'\n')

    if 'EQUIPAMIENTO' in parque:
        print('Equipamiento:\n')
        print(parque['EQUIPAMIENTO']+'\n')

    if 'TRANSPORTE' in parque:
        print('Transporte:\n')
        print(parque['TRANSPORTE']+'\n')

    if 'LOCALIZACION' in parque:
        print('Dirección:\n')
        print(parque['LOCALIZACION']+'\n')

# obtenerDatos()
datos = procesar_XML()
pedir_entrada(datos)
