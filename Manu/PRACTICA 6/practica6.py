# Para el desarrollo Web
from bottle import run, route, error, request, template, static_file, get, post

# Para el Web Scrapping
import re
import requests
from bs4 import BeautifulSoup


# **********************************************************************************************************************

# Clase modelo. Alberga el modelo de datos de la aplicacion.

class Model:
    __instance = None

    def __init__(self):

        self.__userWords = []
        self.__gruposPlantas = {}
        self.__mapaDescripciones = {}
        self.__webs = [
            'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(A-B)',
            'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(C)',
            'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(D-G)',
            'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(H-M)',
            'https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(N-Z)',
        ]

    def getWebs(self):
        return self.__webs

    def getUserWords(self):
        return self.__userWords

    def setUserWords(self, value):
        self.__userWords = value

    def getGruposPlantas(self):
        return self.__gruposPlantas

    def getMapaDescripciones(self):
        return self.__mapaDescripciones

    @staticmethod
    def getInstance():

        if Model.__instance is None:
            Model.__instance = Model()

        return Model.__instance

    def obtainDiseases(self):
        csvFile = open('resources/Enfermedades.csv', encoding="utf-8", errors='ignore')
        import csv
        reader = csv.reader(csvFile, delimiter=";")
        diseases = []
        for data in reader:
            diseases.append("".join(data))
        csvFile.close()
        return diseases

    def obtainDataUsingWebScrapping(self):

        self.__recolectarDatos()

    def orSearchInPlantsDescription(self, words):

        nombresCoincidencias = []

        for word in words:
            nombresCoincidencias.append(self.__buscarCoincidencias(word))

        nombresResultados = self.__union(nombresCoincidencias)

        data = dict()

        # print()
        # print("Se han encontrado", len(nombresResultados), "coincidencias: ")

        for nombre in nombresResultados:
            data[nombre] = self.__mapaDescripciones[nombre]

        return data

    def andSearchInPlantsDescription(self, words):

        nombresCoincidencias = []

        for word in words:
            nombresCoincidencias.append(self.__buscarCoincidencias(word))

        nombresResultados = self.__interseccion(nombresCoincidencias)

        data = dict()

        # print()
        # print("Se han encontrado", len(nombresResultados), "coincidencias: ")

        for nombre in nombresResultados:
            data[nombre] = self.__mapaDescripciones[nombre]

        return data

    def obtainPlantsForDiseases(self, diseases):

        nombresCoincidencias = []

        for disease in diseases:

            for word in disease.split(" "):
                nombresCoincidencias.append(self.__buscarCoincidencias(word))

        nombresResultados = self.__union(nombresCoincidencias)

        data = dict()

        # print()
        # print("Se han encontrado", len(nombresResultados), "coincidencias: ")

        for nombre in nombresResultados:
            data[nombre] = self.__mapaDescripciones[nombre]

        return data

    def __recolectarDatos(self):
        i = 1
        for web in self.__webs:
            # print("Recolectando datos de plantas... (", i, "/", len(self.webs), ")")
            plantas = self.__extraerPlantas(web)
            self.__guardarPlantas(plantas, i)
            i += 1

    def __guardarPlantas(self, plantas, grupo):
        self.__gruposPlantas[grupo] = {}
        i = 1
        for planta in plantas:
            self.__gruposPlantas[grupo][i] = planta
            # print(self.gruposPlantas[grupo][i]);
            i += 1

    def __buscarCoincidencias(self, palabra):
        coincidencias = []
        regexp = re.compile(r"\b" + palabra + r"\b", re.IGNORECASE)
        for planta, descripcion in self.__mapaDescripciones.items():
            if regexp.search(descripcion):
                coincidencias.append(planta)
        return coincidencias

    def __union(self, listas):
        resultado = set()
        for lista in listas:
            resultado = resultado.union(lista)
        return resultado

    def __interseccion(self, listas):
        resultado = set(listas[0])
        for i in range(1, len(listas)):
            resultado = resultado & set(listas[i])
        return resultado

    def __extraerPlantas(self, web):
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

            self.__mapaDescripciones[tituloPlanta.get_text()] = descripcion

        return plantas


# **********************************************************************************************************************

# Clase despachador de vistas. Carga completamente una vista particular y luego la devuelve para poder ser mostrada.

class DispatcherView:
    __instance = None

    @staticmethod
    def getInstance():
        if DispatcherView.__instance is None:
            DispatcherView.__instance = DispatcherView()

        return DispatcherView.__instance

    def generateService(self, data):
        return template('service.tpl', dict=data)

    def generateResultsForService(self, data):
        return template('results.tpl', dict=data)


# **********************************************************************************************************************

# Clase controlador. Gestiona las peticiones que recibe la aplicacion.

class Controller:
    __instance = None

    @staticmethod
    def getInstance():

        if Controller.__instance is None:
            Controller.__instance = Controller()

        return Controller.__instance

    def action(self, context):

        if context["event"] == "INITIALIZE":

            DispatcherView.getInstance()

            Model.getInstance().obtainDataUsingWebScrapping()

        elif context["event"] == "PROVIDE_SERVICE_1_TO_USER":

            context["object"]["webs"] = Model.getInstance().getWebs()

            context["object"]["groupsOfPlants"] = Model.getInstance().getGruposPlantas()

            return DispatcherView.getInstance().generateService(context["object"])

        elif context["event"] == "PROVIDE_SERVICE_1_BIS_TO_USER":

            selectedGroupIndex = context["object"]["selectedGroupIndex"]

            context["object"]["selectedGroup"] = Model.getInstance().getGruposPlantas()[selectedGroupIndex]

            return DispatcherView.getInstance().generateService(context["object"])

        elif context["event"] == "SHOW_SERVICE_1_RESULTS_TO_USER":

            selectedGroupIndex = context["object"]["group"]

            context["object"]["selectedGroup"] = Model.getInstance().getGruposPlantas()[selectedGroupIndex]

            return DispatcherView.getInstance().generateResultsForService(context["object"])

        elif context["event"] == "PROVIDE_SERVICE_2_TO_USER":

            return DispatcherView.getInstance().generateService(context["object"])

        elif context["event"] == "PROVIDE_SERVICE_2_BIS_TO_USER":

            # Si hemos llegado aqui significa que el usuario ha introducido mas de una palabra.

            # El modelo debe de almacenar las palabras que el usuario quiere para ser accedidas mas adelante.
            Model.getInstance().setUserWords(context["object"]["words"])

            # Devolvemos la vista con los radio button para que el usuario pueda escoger el tipo de busqueda.
            return DispatcherView.getInstance().generateService(context["object"])

        elif context["event"] == "SHOW_SERVICE_2_RESULTS_TO_USER":

            # Si hemos llegado aqui signica que o bien el usuario metio una palabra como creiterio
            # de busqueda o bien el usuario metio mas de una palabra y luego selecciono el tipo de busqueda.

            if "searchType" in context["object"]:  # Si el usuario ha introducido varias palabras y un tipo de busqueda.

                userWords = Model.getInstance().getUserWords()  # Hay que recuperar las palabras del modelo.

                if context["object"]["searchType"] == "OR":  # Busqueda OR

                    context["object"]["plants"] = Model.getInstance().orSearchInPlantsDescription(userWords)

                else:  # Busqueda AND

                    context["object"]["plants"] = Model.getInstance().andSearchInPlantsDescription(userWords)

            else:  # El usuario solo ha introducido una unica palabra, se realiza una busqueda OR de esta.

                userWords = context["object"]["words"]

                context["object"]["plants"] = Model.getInstance().orSearchInPlantsDescription(userWords)

            return DispatcherView.getInstance().generateResultsForService(context["object"])

        elif context["event"] == "PROVIDE_SERVICE_3_TO_USER":

            context['object']['diseases'] = Model.getInstance().obtainDiseases()

            return DispatcherView.getInstance().generateService(context["object"])

        elif context["event"] == "SHOW_SERVICE_3_RESULTS_TO_USER":

            context["object"]["plantsForDiseases"] = Model.getInstance().obtainPlantsForDiseases(
                map(lambda x: x.replace('Ã¡','á').replace('Ã©','é').replace('Ã\xad','í').replace('Ã³','ó').replace('Ãº','ú'),context["object"]["diseases"])
            )

            return DispatcherView.getInstance().generateResultsForService(context["object"])


# **********************************************************************************************************************

# Se dispara cuando el usuario quiere hacer uso del servicio 1.
@get('/Servicio1')
def service1():
    return Controller.getInstance().action(
        {
            "event": "PROVIDE_SERVICE_1_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 1",
                    "serviceNameToShow": "SERVICIO 1"
                }
        }
    )


# Se dispara para que el usuario decida que grupo de plantas quiere consultar.
@post('/Servicio1Bis')
def service1Bis():
    return Controller.getInstance().action(
        {
            "event": "PROVIDE_SERVICE_1_BIS_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 1 BIS",
                    "serviceNameToShow": "SERVICIO 1",
                    "selectedGroupIndex": int(request.forms.grupo)
                }
        }
    )


# Se dispara cuando es el momento de mostrarle al usuario los datos.
@post('/Service1Results')
def service1Results():
    groupPlant = request.forms.get("group:plant")

    return Controller.getInstance().action(
        {
            "event": "SHOW_SERVICE_1_RESULTS_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 1",
                    "serviceNameToShow": "SERVICIO 1",
                    "group": int(groupPlant.split(":")[0]),
                    "plant": int(groupPlant.split(":")[1])
                }
        }
    )


# Se dispara cuando el usuario quiere hacer uso del servicio 2.
@get('/Servicio2')
def service2():
    return Controller.getInstance().action(
        {
            "event": "PROVIDE_SERVICE_2_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 2",
                    "serviceNameToShow": "SERVICIO 2"
                }
        }
    )


# Se dispara cuando es el momento de mostrarle al usuario los datos.
# Se dispara para que el usuario decida que tipo de busqueda desea realizar.
@post('/Servicio2Bis')
def service2Bis():
    words = request.forms.palabras.split(" ")

    return Controller.getInstance().action(
        {
            "event": "PROVIDE_SERVICE_2_BIS_TO_USER" if (len(words) > 1) else "SHOW_SERVICE_2_RESULTS_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 2 BIS" if (len(words) > 1) else "SERVICIO 2",
                    "serviceNameToShow": "SERVICIO 2",
                    "words": words
                }
        }
    )


# Se dispara cuando es el momento de mostrarle al usuario los datos.
@post('/Service2Results')
def service2Results():
    return Controller.getInstance().action(
        {
            "event": "SHOW_SERVICE_2_RESULTS_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 2",
                    "serviceNameToShow": "SERVICIO 2",
                    "searchType": request.forms.tipoBusqueda
                }
        }
    )


# Se dispara cuando el usuario quiere hacer uso del servicio 3.
@get('/Servicio3')
def service3():
    return Controller.getInstance().action(
        {
            "event": "PROVIDE_SERVICE_3_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 3",
                    "serviceNameToShow": "SERVICIO 3"
                }
        }
    )


# Se dispara cuando es el momento de mostrarle al usuario los datos.
@post('/Service3Results')
def service3Results():
    return Controller.getInstance().action(
        {
            "event": "SHOW_SERVICE_3_RESULTS_TO_USER",
            "object":
                {
                    "serviceName": "SERVICIO 3",
                    "serviceNameToShow": "SERVICIO 3",
                    "diseases": ["".join(disease) for disease in request.forms]
                }
        }
    )


# Nodo/Pagina principal del servidor.
@get('/')
def main():
    return static_file('resources/main.html',root='')


# Estos metodos se han contruido para proporcionar ficheros estaticos.
@get("/css/<filepath:re:.*\\.css>")
def css(filepath):
    return static_file(filepath, root="public/css")


@get("/img/<filepath:re:.*\\.(jpg|png|gif|ico|svg)>")
def css(filepath):
    return static_file(filepath, root="public/img")


# Cuando la pagina no se encuentra.
@error(404)
def error404():
    return "LA PAGINA SOLICITADA NO HA SIDO ENCONTRADA"


# **********************************************************************************************************************

Controller.getInstance().action({"event": "INITIALIZE", "object": None})

run(host='localhost', port=8080, debug=True)