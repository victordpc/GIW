
import urllib
from bs4 import BeautifulSoup
import re
import requests


def procesar_webs(url_indice, lista_ignorar_claves):
    '''Procesa todas las páginas recibidas para obtener los datos limpios
    '''
    datos = dict()
    for nombre, url in url_indice.items():
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')

        plantas = soup.find('div', class_='mw-parser-output')
        etiquetas_h3 = limpiar_etiqueta_h3(
            plantas.find_all(re.compile('(h3)')))
        etiquetas_h3 = list(
            filter(lambda x: x not in lista_ignorar_claves, etiquetas_h3))
        etiquetas_dl = limpiar_etiqueta_dl(
            plantas.find_all(re.compile('(dl)')))

        elementos = dict()
        for i in range(len(etiquetas_dl)):
            elementos[etiquetas_h3[i]] = 'Planta:\n\n' + \
                etiquetas_h3[i]+'\n\n' + etiquetas_dl[i]

        datos[nombre] = elementos
    return datos


def limpiar_etiqueta_h3(etiquetas):
    '''Limpia el contenido de las etiquetas h3
    '''
    etiquetas = list(map(lambda x: x.span.next_sibling.string if x.span.string ==
                         None else x.span.string, etiquetas))
    return etiquetas


def limpiar_etiqueta_dl(etiquetas):
    '''Limpia el contenido de las etiquetas dl
    '''
    datos = list()
    for etiqueta in etiquetas:
        cadena = ''
        nombre_cientifico = 'Nombre científico:\n\n'
        descripcion = '\n\nDescripción:\n\n'

        for coso in etiqueta.children:

            if coso.name == 'dt':
                if coso.string != None:
                    nombre_cientifico = nombre_cientifico + coso.string
                else:
                    nombre_cientifico = nombre_cientifico + coso.text
            elif coso.name == 'dd':
                descripcion = descripcion+coso.text+'\n'

        descripcion = re.compile(r'(\[\d*\])').sub('', descripcion)
        cadena = nombre_cientifico+descripcion+'\n'
        datos.append(cadena)

    return datos


def filtrar_or(palabras, datos):
    cadena = '('+palabras[0]+')+'
    for i in range(1, len(palabras)):
        cadena = cadena + '|('+palabras[i]+')+'

    cadena = re.compile(cadena, re.IGNORECASE)
    for conjunto in datos.values():
        filtro_salida = list(
            filter(cadena.search, list(conjunto.values())))
        for salida in filtro_salida:
            print(salida.strip())


def filtrar_and(palabras, datos):
    ''' Filtra los datos en función de las palabras recibidas usando la interseccion de los resultados parciales 
    '''
    filtro_salida = list()
    cadena = '('+palabras[0]+')'
    cadena = re.compile(cadena, re.IGNORECASE)

    for conjunto in datos.values():
        filtro_salida.extend(
            list(filter(cadena.search, list(conjunto.values()))))

    for i in range(1, len(palabras)):
        cadena = '('+palabras[i]+')'
        cadena = re.compile(cadena, re.IGNORECASE)
        filtro_salida = list(
            filter(cadena.search, filtro_salida))

    return filtro_salida


def menu_indice(datos, nombres_indice, url_indice):
    '''Muestra el submenú cuando seleccionamos búsqueda por indice
    '''
    print('\nSeleccione una opción:')
    for clave in url_indice.keys():
        print(clave)
    op2 = input()

    print('\nSeleccione una planta:')
    a = 1
    for etiqueta in datos[nombres_indice[int(op2)]].keys():
        print('('+str(a)+') '+etiqueta)
        a = a+1

    op3 = input()

    nombre_planta = list(datos[nombres_indice[int(op2)]].keys())[int(op3)-1]
    descripcion_planta = datos[nombres_indice[int(op2)]][nombre_planta]
    print(descripcion_planta)


def menu_clave(datos, nombres_indice, url_indice):
    '''Muestra el submenú cuando seleccionamos búsqueda por clave
    '''
    palabras = input(
        '\n Introduzca las claves por las que quiere realizar la búsqueda\n')
    palabras = palabras.split(' ')

    op_join = 0
    if len(palabras) > 1:
        op_join = input('\nHa introducido varias palabras para busqueda, como quiere realizarla:\n(1) AND plantas donde aparecen todas las palabras introducidas\n(2) OR plantas donde aparece alguna de las palabras introducidas\n')

    if op_join == str(1):
        filtro_salida = filtrar_and(palabras, datos)
        for elemento in filtro_salida:
            print(elemento.strip())

    else:
        filtrar_or(palabras, datos)


def main():
    '''Función main del programa
    '''
    nombres_indice = ['(1) Plantas_medicinales_(A-B)', '(2) Plantas_medicinales_(C)',
                      '(3) Plantas_medicinales_(D-G)', '(4) Plantas_medicinales_(H-M)', '(5) Plantas_medicinales_(N-Z)']
    url_indice = {'(1) Plantas_medicinales_(A-B)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(A-B)',
                  '(2) Plantas_medicinales_(C)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(C)',
                  '(3) Plantas_medicinales_(D-G)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(D-G)',
                  '(4) Plantas_medicinales_(H-M)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(H-M)',
                  '(5) Plantas_medicinales_(N-Z)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(N-Z)'}
    lista_ignorar_claves = ['Notas y referencias', 'Notas',
                            'Referencias', 'Ver también', 'Bibliografía', 'Véase también']

    datos = procesar_webs(url_indice, lista_ignorar_claves)

    continuar = True
    while(continuar):
        op1 = input(
            'Seleccione el tipo de búsqueda que desea realizar:\n (1) Indice\n (2) Clave\n')

        if (op1 == '1' or op1.upper() == 'INDICE'):
            menu_indice(datos, nombres_indice, url_indice)
        if (op1 == '2' or op1.upper() == 'CLAVE'):
            menu_clave(datos, nombres_indice, url_indice)

        op2 = input(
            '\n\n¿Desea realizar otra búsqueda?\n(1). Si\n(2). Finalizar programa\n')

        if op2 == '2':
            continuar = False


main()
