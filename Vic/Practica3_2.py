from xml.etree import ElementTree


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
                        if direccion.text != None:
                            nombre_via = direccion.text.strip()
                        else:
                            nombre_via = ''
                    elif 'CLASE-VIAL' == direccion.attrib['nombre']:
                        if direccion.text != None:
                            tipo_via = direccion.text.strip()+' '
                        else:
                            tipo_via = ''
                    elif 'NUM' == direccion.attrib['nombre']:
                        if direccion.text != None:
                            numero = ', ' + direccion.text.strip()
                        else:
                            numero = ''
                    elif 'LOCALIDAD' == direccion.attrib['nombre']:
                        if direccion.text != None:
                            localidad = '. ' + direccion.text.strip()
                        else:
                            localidad = ''
                    elif 'PROVINCIA' == direccion.attrib['nombre']:
                        if direccion.text != None:
                            provincia = '. ' + direccion.text.strip()
                        else:
                            provincia = ''
                    elif 'CODIGO-POSTAL' == direccion.attrib['nombre']:
                        if direccion.text != None:
                            codigo_postal = ', ' + direccion.text.strip()
                        else:
                            codigo_postal = ''

                    if direccion.text != None:
                        parque[direccion.attrib['nombre']
                               ] = direccion.text.strip()

                cadena = (tipo_via + nombre_via + numero +
                          localidad + provincia + codigo_postal).strip()

                if cadena != "":
                    parque[elementos.attrib['nombre']] = cadena

            else:
                if elementos.text != None:
                    parque[elementos.attrib['nombre']] = elementos.text.strip()

        datos[parque['NOMBRE']] = parque
    return datos


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


def preguntar_filtros():
    datos = dict()
    print('\nIntroduzca los campos a filtar:\n')
    print('Accesibilidad: ', end='')
    datos['Accesibilidad'] = input()
    print('Nombre: ', end='')
    datos['Nombre'] = input()
    print('Barrio: ', end='')
    datos['Barrio'] = input()
    print('Distrito: ', end='')
    datos['Distrito'] = input()
    return datos


def filtrar_datos(datos, filtro):
    resultado = list()
    for clave, valores in datos.items():
        for clave_filtro, valor_filtro in filtro.items():
            if filtro[clave_filtro] != '' and clave_filtro.upper() in valores and valores[clave_filtro.upper()].find(valor_filtro) > -1:
                resultado.append(clave)

    return resultado


datos = procesar_XML()
filtro = preguntar_filtros()
parques = filtrar_datos(datos, filtro)
for parque in parques:
    mostrar_informacion(datos[parque])
