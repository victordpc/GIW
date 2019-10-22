
import urllib
from bs4 import BeautifulSoup
import re
import requests

def buscar_lista_indices(url):
    lista_ignorar_claves=['Notas y referencias','Notas','Referencias','Ver también','Bibliografía']

    html=urllib.request.urlopen(url).read()
    soup=BeautifulSoup(html, 'html.parser')

    etiquetas=soup.find_all('span',class_='toctext')
    etiquetas= map(lambda x: x.string,etiquetas)
    
    etiquetas = list(filter(lambda x: x not in lista_ignorar_claves,etiquetas))
    
    return etiquetas,soup

def mostar_datos_planta(datos):
    print(datos)


# html=urllib.request.urlopen('https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(A-B)').read()

html = requests.get('https://es.wikipedia.org/wiki/Anexo:Plantas_medicinales_(A-B)').text

soup=BeautifulSoup(html, 'html.parser')
seleccion='Bacche'

plantas=soup.find('div', class_='mw-parser-output')

continuar = True
elemento=plantas.find_all(re.compile('(h3)|(dl)'))
print(elemento)
