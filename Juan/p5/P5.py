import re
import requests
from bs4 import BeautifulSoup

webs = [
    'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(A-B)',
    'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(C)',
    'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(D-G)',
    'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(H-M)',
    'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(N-Z)',
]

gruposPlantas = {}
mapaDescripciones = {}


def extraerPlantas(web):
    req = requests.get(web)
    soup = BeautifulSoup(req.text, "html.parser")
    [tag.extract() for tag in soup.select('.reference')]
    itemsLista = soup.select('#toc > ul li > a')
    plantas = []
    for item in itemsLista:
        idPlanta = item['href'].replace('#', '')
        tituloPlanta = soup.find(id=idPlanta)
        if tituloPlanta.parent.name != 'h3':
            continue

        infoPlanta = tituloPlanta.parent.find_next_sibling('dl')
        if infoPlanta is None:
            continue

        nombreCientifico = infoPlanta.select_one('p a,dt a')
        if nombreCientifico is None:
            nombreCientifico = 'Desconocido'
        else:
            nombreCientifico = nombreCientifico.get_text().strip()

        bloquesInfo = infoPlanta.findChildren()

        if infoPlanta.name == 'p':
            descripcion = infoPlanta.find_next_sibling().get_text().strip()
        elif len(bloquesInfo) > 0:
            bloquesInfo[0].extract()
            descripcion = infoPlanta.get_text().strip()

        plantas.append({
            "nombre": tituloPlanta.get_text(),
            "nombre_cientifico": nombreCientifico,
            "descripcion": descripcion
        })
        mapaDescripciones[tituloPlanta.get_text()] = descripcion
    return plantas


def guardarPlantas(plantas, grupo):
    gruposPlantas[grupo] = {}
    i = 1
    for planta in plantas:
        gruposPlantas[grupo][i] = planta
        i += 1


def mostrarMenu():
    print("1. Buscar por índice")
    print("2. Buscar por palabra clave")
    print("0. Salir")


def mostrarDatosPlanta(planta):
    print()
    print("Planta: ")
    print(planta['nombre'])
    print()

    print("Nombre científico: ")
    print(planta['nombre_cientifico'])
    print()

    print("Descripción: ")
    print(planta['descripcion'])
    print()


def buscarPorIndice():
    print("1. Plantas medicinales (A-B)")
    print("2. Plantas medicinales (C)")
    print("3. Plantas medicinales (D-G)")
    print("4. Plantas medicinales (H-M)")
    print("5. Plantas medicinales (N-Z)")
    grupo = recogerOpcion()
    i = 1
    a = gruposPlantas.keys()
    for planta in gruposPlantas[grupo].values():
        print(i, ".", planta['nombre'])
        i += 1
    planta = recogerOpcion()
    mostrarDatosPlanta(gruposPlantas[grupo][planta])
    print("¿Desea realizar una nueva búsqueda? (1 sí, 0 no)")
    continuar = recogerOpcion()
    if continuar == 1:
        buscarPorIndice()


def buscarCoincidencias(palabra):
    coincidencias = []
    regexp = re.compile(r"\b" + palabra + r"\b", re.IGNORECASE)
    for planta, descripcion in mapaDescripciones.items():
        if regexp.search(descripcion):
            coincidencias.append(planta)
    return coincidencias


def interseccion(listas):
    resultado = set(listas[0])
    for i in range(1, len(listas)):
        resultado = resultado & set(listas[i])
    return resultado


def union(listas):
    resultado = set()
    for lista in listas:
        resultado = resultado.union(lista)
    return resultado


def mostrarResultados(resultados):
    print()
    print("Se han encontrado", len(resultados), "coincidencias: ")
    for nombre in resultados:
        print('Planta:', nombre)
        print('Descripción:', mapaDescripciones[nombre])
        print()


def buscarPorPalabraClave():
    palabras = input("Introduzca las palabras de búsqueda separadas por espacios:")
    palabras = palabras.split(' ')

    tipoBusqueda = ''
    if len(palabras) > 1:
        tipoBusqueda = input("Ha introducido más de una palabra, ¿Quiere hacer una búsqueda AND (1) u OR (0)?")

    nombresCoincidencias = []
    for palabra in palabras:
        nombresCoincidencias.append(buscarCoincidencias(palabra))

    if len(palabras) > 1:
        if tipoBusqueda == '1':
            nombresResultados = interseccion(nombresCoincidencias)
        else:
            nombresResultados = union(nombresCoincidencias)
    else:
        nombresResultados = [val for sublista in nombresCoincidencias for val in sublista]

    mostrarResultados(nombresResultados)
    print("¿Desea realizar una nueva búsqueda? (1 sí, 0 no)")
    continuar = recogerOpcion()
    if continuar == 1:
        buscarPorPalabraClave()


def recogerOpcion():
    value = int(input("Introduzca una opcion: "))
    return value


def ejecutarOpcion(opcion):
    if opcion == 1:
        buscarPorIndice()
    elif opcion == 2:
        buscarPorPalabraClave()


def recolectarDatos():
    i = 1
    for web in webs:
        print("Recolectando datos de plantas... (", i, "/", len(webs), ")")
        plantas = extraerPlantas(web)
        guardarPlantas(plantas, i)
        i += 1


def main():
    recolectarDatos()
    continuar = True
    while continuar:
        mostrarMenu()
        opcion = recogerOpcion()
        continuar = opcion != 0
        if continuar:
            ejecutarOpcion(opcion)


main()
