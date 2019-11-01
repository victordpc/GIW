from bottle import route, run, template, get, post,request
import re
import requests
from bs4 import BeautifulSoup

# Se pide crear una aplicación web que tenga una página principal que mostrará un
# conjunto enlaces que representan los servicios que ofrece la aplicación[1 punto]:


@route('/')
def index():
    output = template("plantillas_web/index")
    return output


# Servicio 1: Mostrar información sobre una planta seleccionada. Cuando el usuario
# pulsa sobre el servicio 1 se le mostrará un formulario en el que dispondrá varios
# desplegables donde podrá seleccionar la planta. Un seleccionable para elegir el
# grupo , y otro para seleccionar la planta del grupo que ha elegido. Cuando pulse
# sobre un botón de tipo "Enviar", se le mostrará una nueva página que mostrará la
# descripción de la planta. En la página del formulario como en la del resultado
# habrá un enlace para volver a la página inicial[3 puntos]


@route('/servicio1.html')
def servicio1():
    output = template("plantillas_web/servicio1", lista=titulos)
    return output


@route('/servicio11.html', method="POST")
def servicio11():
    variable=request
    output = template("plantillas_web/servicio1", lista=titulos)
    return output


# @route('/login', method="POST")
# def do_login():
#     username = request.forms.get("username")
#     password = request.forms.get("password")
#     if check_login(username, password):
#         return "<p> Tu información de login es correct.</p>"
#     else:
#         return "<p>Login fallado</p>"

# Servicio 2:Buscar planta por palabra clave. Si elige esta opción se le pedirá al
# usuario que introduzca un conjunto de palabras que se utilizarán para realizar
# una búsqueda sobre el texto de las descripciones asociadas a las plantas que
# aparecen en cada página. A continuación, si ha introducido más de una palabra,
# se le preguntará si quiere realizar una búsqueda de tipo "AND" o una búsqueda
# de tipo "OR", es decir si busca plantas donde aparece todas las palabras
# introducidas o si busca plantas donde aparecen alguna de las palabras
# introducidas. Cuando pulse sobre un botón de tipo "Enviar", se le mostrará una
# nueva página con un listado de todas las plantas junto a las descripciones de las
# mismas que cumplen las condiciones de búsqueda. En la página del formulario como
# en la del resultado habrá un enlace para volver a la página inicial[3 puntos]


@route('/servicio2.html')
def servicio2():
    output = template("plantillas_web/servicio2")
    return output


# Servicio 3:Buscar plantas por enfermedades. Si elige esta opción se le mostrará
# un listado chequeable donde seleccionará una o más enfermedades. Cuando pulse
# sobre un botón de tipo "Enviar", se le mostrará una nueva página con todas las
# plantas que pueden venir bien para esa enfermedad. Para ello se proporciona junto
# a la práctica un csv con nombres de enfermedades que servirá de entrada para
# generar el listado de enfermedades.En la página del formulario como en la del
# resultado habrá un enlace para volver a la página inicial[3 puntos]
# Arranque del servidor


@route('/servicio3.html')
def servicio3():
    output = template("plantillas_web/servicio3")
    return output


webs = {
    'Plantas_medicinales_(A-B)':  'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(A-B)',
    'Plantas_medicinales_(C)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(C)',
    'Plantas_medicinales_(D-G)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(D-G)',
    'Plantas_medicinales_(H-M)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(H-M)',
    'Plantas_medicinales_(N-Z)': 'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(N-Z)',
}

titulos = {
    'Plantas_medicinales_(A-B)',
    'Plantas_medicinales_(C)',
    'Plantas_medicinales_(D-G)',
    'Plantas_medicinales_(H-M)',
    'Plantas_medicinales_(N-Z)',
}


gruposPlantas = {}
mapaDescripciones = {}


def extraerPlantas(web):
    req = requests.get(web)
    soup = BeautifulSoup(req.text, "html.parser")
    # html = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(html, "html.parser")
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
        mapaDescripciones[tituloPlanta.get_text()] = re.compile(
            r'(\[\d*\])').sub('', descripcion).strip()
    return plantas


def guardarPlantas(plantas, grupo):
    gruposPlantas[grupo] = {}
    for planta in plantas:
        gruposPlantas[grupo][planta['nombre']] = planta


def recolectarDatos():
    i = 0
    for nombre, web in webs.items():
        print("Recolectando datos de plantas... (", i, "/", len(webs), ")")
        plantas = extraerPlantas(web)
        guardarPlantas(plantas, nombre)
        i = i+1


recolectarDatos()

run(host='0.0.0.0', port=8080)
